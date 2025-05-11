from logger import Logger


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
        self.nane = program['name']
        self.schedule_time = {
            "H": program['schedule_time'].split(':')[0],
            "M": program['schedule_time'].split(':')[1]
        }
        self.week_days = self.format_weekdays(program.get('week_days', 'LMXJVSD'))
        self.wether_adjustment = program.get('wether_adjustment', False)
        self.run_time = program.get('run_time')

