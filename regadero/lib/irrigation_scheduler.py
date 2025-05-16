from time import localtime as t_localtime, mktime as t_mktime, sleep as t_sleep

import _thread

from logger import Logger
from utils import datetime

class Program():

    logger = None

    name:str = None
    schedule_time:dict = None
    week_days:str = None  # "0123456"
    wether_adjustment:bool = False
    run_time:int = None
    zones:list[dict] = None
    enabled = True

    stopped = False
    executing = False
    wait_time = 1 * 60

    def __init__(self, program:dict) -> None:
        """
        program dict properties:

            * every (str): [NUM] DAY|HOUR
            * name (str): name for the program
            * schedule_time (str with format HH:MM): time for the program to start
            * week_days (str with format, defualt: LMXJVSD): week days for the program to start
            * wether_adjustment (bool default true): adjust times with prediccion data
            * time (int): time in minutes to be used as default value on the zones.
            * zones (list[dict]): Zone specification

        zone dict properties:
            * name (str): name of the zone
            * time (int): Time in minutes for the zone to run
            * enabled (bool, default false): if the irrigation is enabled on this zone.
        """

        self.logger = Logger("program")
        self.logger.info(f"initializing program '{program.get('name')}'")
        self.name = program['name']
        self.enabled = program.get('enabled', True)
        self.schedule_time = {
            "H": int(program['schedule_time'].split(':')[0]),
            "M": int(program['schedule_time'].split(':')[1])
        }
        self.week_days = program.get('week_days', '0123456')
        self.wether_adjustment = program.get('wether_adjustment', False)
        self.run_time = program.get('run_time', 0)
        self.zones = program['zones']

        self.logger.info("program is: %s" % program)
        self.logger.info(f"program '{self.name}' basic config:")
        self.logger.info(f"  > schedule_time: {self.schedule_time}")
        self.logger.info(f"  > week_days: {self.week_days}")
        self.logger.info(f"  > wether_adjustment: {self.wether_adjustment}")
        self.logger.info(f"  > run_time: {self.run_time}")
        self.logger.info(f"  > {len(self.zones)} zones loaded")

        self.set_next_run_datetime()


    def set_next_run_datetime(self):
        (Y, M, D, h, m, s, wd, yd) = t_localtime()

        now = (Y, M, D, h, m, s, None, None)
        self.logger.info(f" now is {datetime(t_mktime(now))}")

        self.logger.info(f"run time is {self.schedule_time['H']}:{self.schedule_time['M']}")
        next_run = (Y, M, D, self.schedule_time['H'], self.schedule_time['M'], 0, None, None)
        self.logger.info(f" nex run  will be at {datetime(t_mktime(next_run))}")

        self.next_run_datetime = t_mktime(next_run)
        if t_mktime(now) > t_mktime(next_run):
            ## always executed every day for now:
            self.next_run_datetime += 86400
            self.logger.info(f"next run time will be tomorrow")

        self.logger.info(f"next run is at {datetime(self.next_run_datetime)}")

    def irrigation(self):
        self.logger.info("Start irrigation of program %s" % self.name)
        for zone in self.zones:
            if zone.get('enabled', True):
                self.logger.info(f"  >> Starting irrigation on zone {zone['name']} during: {zone.get('run_time', self.run_time)} minutes")
                # do whatever to enable irrigation
                t_sleep(zone.get('run_time', self.run_time))
                self.logger.info(f"  << Irrigation on zone {zone['name']} finish")
            else:
                self.logger.info(f"  -- Irrigation on zone {zone['name']} is disabled")
        self.logger.info("Irrigation of program %s finished!!" % self.name)


    def run_schedule(self):
        if not self.enabled:
            self.logger.info("program '%s' is not enabled" % self.name)
            return
        self.logger.info("Starting program '%s'" % self.name)

        while not self.stopped and self.enabled:
            (Y, M, D, h, m, s, wd, yd) = t_localtime()
            now = t_mktime((Y, M, D, h, m, s, wd, None))
            self.logger.debug(f"  >> checking program '{self.name}' - next run is at {datetime(self.next_run_datetime)} on days {self.week_days}")
            if  now > self.next_run_datetime and f"{wd}" in self.week_days:
                self.logger.info(f"Running program at {datetime(now)}!!")
                self.executing = True
                self.irrigation()
                self.executing = False
                self.set_next_run_datetime()
                self.logger.debug(f"next run will be at ({self.next_run_datetime}) {datetime(self.next_run_datetime)}")
            t_sleep(self.wait_time)
        self.logger.warning(f"Program '{self.name}' has been  stopped or disabled!! {self.stopped} {self.enabled}")

    def start(self):
        return _thread.start_new_thread(self.run_schedule, ())

    def stop(self):
        self.logger.warning("Stoping program %s!!" % self.name)
        self.stopped = True
