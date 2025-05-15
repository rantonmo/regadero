from time import localtime as t_localtime, mktime as t_mktime, sleep as t_sleep

from logger import Logger
from utils import datetime

class Program():

    logger = None

    name:str = None
    schedule_time:dict = None
    week_days:str = None  # "0123456"
    wether_adjustment:bool = False
    run_time:int = None

    def __init__(self, program:dict) -> None:
        """
        program dict properties:

            * type (str): daily
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
        self.schedule_time = {
            "H": int(program['schedule_time'].split(':')[0]),
            "M": int(program['schedule_time'].split(':')[1])
        }
        self.week_days = program.get('week_days', '0123456')
        self.wether_adjustment = program.get('wether_adjustment', False)
        self.run_time = program.get('run_time')

        self.logger.info("program is: %s" % program)
        self.logger.info(f"program '{self.name}' basic config:")
        self.logger.info(f"  > schedule_time: {self.schedule_time}")
        self.logger.info(f"  > week_days: {self.week_days}")
        self.logger.info(f"  > wether_adjustment: {self.wether_adjustment}")
        self.logger.info(f"  > run_time: {self.run_time}")

        self.next_run_datetime = self.get_next_run_datetime()


    def get_next_run_datetime(self):
        (Y, M, D, h, m, s, wd, yd) = t_localtime()

        now = (Y, M, D, h, m, s, None, None)
        self.logger.info(f" now is {datetime(t_mktime(now))}")

        self.logger.info(f"run time is {self.schedule_time['H']}:{self.schedule_time['M']}")
        next_run = (Y, M, D, self.schedule_time['H'], self.schedule_time['M'], 0, None, None)
        # next_run = now = (Y, M, D, 2, 0, 0, None, None)
        self.logger.info(f" nex run  will be at {datetime(t_mktime(next_run))}")

        self.next_run_datetime = t_mktime(next_run)
        if t_mktime(now) > t_mktime(next_run):
            self.logger.info(f"next run time will be tomorrow")
            self.next_run_datetime = self.next_run_datetime + 86400

        self.logger.info(f"next run is at {datetime(self.next_run_datetime)}")


    def start_program(self):
        self.logger.info("Starting program %s" % self.name)


        while True:
            now = t_mktime(t_localtime())
            self.logger.info(f" - checking program {self.name} at {datetime(now)}")
            self.logger.info(f"  >> next run is at {datetime(self.next_run_datetime)}")
            if  now > self.next_run_datetime:
                self.logger.info(f"time to run program: {datetime(now)}")
            t_sleep(1 * 60)
