from os import mkdir as os_mkdir
from time import localtime as t_localtime, mktime as t_mktime, sleep as t_sleep
from json import dumps as j_dumps
import _thread



from gpio_manager import GpioManager
from logger import Logger
from telegram_bot import TelegramBot
from utils import datetime, isdir

class Program():

    logger = None
    gpio = None
    bot = None
    bot_errors = 0

    name:str = None
    schedule_time:dict = None
    iteration = None
    week_days:str = None  # "0123456"
    wether_adjustment:bool = False
    run_time:int = None
    zones:list[dict] = None
    enabled = True

    stopped = False
    executing = False
    wait_time = 1 * 60

    def __init__(self, program:dict, gpio:GpioManager, bot:TelegramBot=None) -> None:
        """
        program dict properties:

            * name (str): name for the program
            * schedule_time (str with format HH:MM): time for the program to start
            * iteration (str): [NUM] DAY|HOUR  -- NOT YET IMPLEMENTED
            * week_days (str with format, defualt: 0123456): week days for the program to start
            * wether_adjustment (bool default true): adjust times with prediccion data
            * time (int): time in minutes to be used as default value on the zones.
            * zones (list[dict]): Zone specification

            zone dict properties:
                * name (str): name of the zone
                * time (int): Time in minutes for the zone to run
                * enabled (bool, default false): if the irrigation is enabled on this zone.

        gpio GpioManager: object to manage leds, switches and buzzer

        bot TelegramBot (optionas): To send Telegram notifications


        """

        self.logger = Logger("program")
        self.logger.info(f"initializing program '{program.get('name')}'")
        self.name = program['name']
        self.enabled = program.get('enabled', True)
        self.schedule_time = {
            "H": int(program['schedule_time'].split(':')[0]),
            "M": int(program['schedule_time'].split(':')[1])
        }
        self.iteration = program.get("iteration", "1 day")  # IGNORED, NOT YET IMPLEMENTED
        self.week_days = program.get('week_days', '0123456')
        self.wether_adjustment = program.get('wether_adjustment', False)
        self.run_time = program.get('run_time', 0)
        self.zones = program['zones']

        if bot:
            self.bot = bot
            self.logger.debug("bot is enabled")

        self.gpio = gpio

        self.logger.info("program is: %s" % program)
        self.logger.info(f"program '{self.name}' basic config:")
        self.logger.info(f"  > schedule_time: {self.schedule_time}")
        self.logger.info(f"  > week_days: {self.week_days}")
        self.logger.info(f"  > wether_adjustment: {self.wether_adjustment}")
        self.logger.info(f"  > run_time: {self.run_time}")
        self.logger.info(f"  > {len(self.zones)} zones loaded")
        self.set_next_run_datetime()
        self.logger.info("program has been initialized")


    def save(self, path="/programs"):
        " save program to file "
        if not isdir(path):
            os_mkdir(path)

        with open(f"{path}/{self.name.lower().replace(' ', '_')}.json", 'w') as __f:
            __f.write(j_dumps({
                    "name": self.name,
                    "enabled": self.enabled,
                    "iteration": self.iteration,
                    "schedule_time": self.schedule_time,
                    "week_days": self.week_days,
                    "wether_adjustment": self.wether_adjustment,
                    "run_time": self.run_time,
                    "zones": self.zones
                }))


    def notify(self, message, notify=True):

        self.logger.info(f"NOTIFY: {message}")
        if self.bot:
            try:
                self.bot.send_message(
                    message, notify=notify)
                self.bot_errors = 0
            except OSError as exc:
                self.logger.error(f"Error sending telegram message: {exc}")
                self.bot_errors += 1
                if self.bot_errors > 5:
                    self.bot = None
                    self.logger.error("too many errors using bot! Disabling...")

    def set_next_run_datetime(self):
        (Y, M, D, h, m, s, wd, yd) = t_localtime()

        now = (Y, M, D, h, m, s, None, None)
        self.logger.info(f" now is {datetime(t_mktime(now))}")

        self.logger.info(f"run time is {self.schedule_time['H']}:{self.schedule_time['M']}")
        next_run = (Y, M, D, self.schedule_time['H'], self.schedule_time['M'], 0, None, None)
        self.logger.info(f" nex run  will be at {datetime(t_mktime(next_run))}")

        self.next_run_datetime = t_mktime(next_run)
        if t_mktime(now) > t_mktime(next_run):
            self.next_run_datetime += 86400
            self.logger.info(f"next run time will be tomorrow")

        self.logger.info(f"next run is at {datetime(self.next_run_datetime)}")

    def irrigation(self):
        self.logger.info("Start irrigation of program %s" % self.name)
        for zone in self.zones:
            if zone.get('enabled', True):
                self.notify(f"  >> Starting irrigation on zone {zone['name']} "
                            f"during: {zone.get('run_time', self.run_time)} minutes")
                self.gpio.start_blink_led('blue', 'sfast')
                t_sleep(60 * zone.get('run_time', self.run_time))
                self.gpio.stop_blink_led('blue')
                self.notify(f"  << Irrigation on zone {zone['name']} finish")
            else:
                self.notify(f"  -- Irrigation on zone {zone['name']} is disabled")
        self.logger.info("Irrigation of program %s finished!!" % self.name)


    def run_schedule(self):
        if not self.enabled:
            self.logger.info("program '%s' is not enabled" % self.name)
            return
        self.logger.info("Starting program '%s'" % self.name)

        while not self.stopped and self.enabled:
            (Y, M, D, h, m, s, wd, yd) = t_localtime()
            now = t_mktime((Y, M, D, h, m, s, wd, None))
            self.logger.debug(f"  >> checking program '{self.name}' - "
                              f"next run is at {datetime(self.next_run_datetime)} "
                              f"- on days {self.week_days}")
            if  now > self.next_run_datetime and f"{wd}" in self.week_days:
                self.notify(f"Running program {self.name}")
                self.executing = True
                self.irrigation()
                self.executing = False
                self.set_next_run_datetime()
                self.notify(f"End run program {self.name} - next run "
                            f"at {datetime(self.next_run_datetime)} on days {self.week_days}")
            t_sleep(self.wait_time)
        self.notify(f"Program '{self.name}' has been stopped or disabled!!"
                    f" stopped: {self.stopped} enabled: {self.enabled}")

    def start(self):
        self.notify(f"program {self.name} started - next run: {datetime(self.next_run_datetime)}")
        return _thread.start_new_thread(self.run_schedule, ())

    def stop(self):
        self.notify(f"Stopping program {self.name}!!")
        self.stopped = True
