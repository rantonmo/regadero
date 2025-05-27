
from os import rename as f_rename, listdir
from time import sleep as t_sleep
from _thread import start_new_thread
from utils import f_exists, datetime

LOGGERS = []

class Logger():

    filename = None
    path = None
    name = None
    sch_rotate_logs = False

    def __init__(self, name="root", filename="regadero.log", path="logs", rotate=False):
        self.filename = filename
        self.path = path
        self.name = name

        if name == "root":
            self.rotate_logs()
        if name == 'root' and rotate:
            self.start_rotate_logs()

        LOGGERS.append(self)
        self.info(f"Logger {name} initialized ({len(LOGGERS)})")

    def rotate_logs(self):
        if f_exists(f"{self.path}/{self.filename}.2"):
            f_rename(f"{self.path}/{self.filename}.2", f"{self.path}/{self.filename}.3")

        if f_exists(f"{self.path}/{self.filename}.1"):
            f_rename(f"{self.path}/{self.filename}.1", f"{self.path}/{self.filename}.2")

        if f_exists(f"{self.path}/{self.filename}"):
            f_rename(f"{self.path}/{self.filename}", f"{self.path}/{self.filename}.1")

        self.info("logs has been rotated")

    def start_rotate_logs(self):
        if self.name != 'root':
            return
        self.sch_rotate_logs = True
        start_new_thread(self._start_rotate_logs, ())

    def stop_rotate_logs(self):
        self.sch_rotate_logs = False

    def _start_rotate_logs(self, hours=24):
        self.info(f"starting rotate logs schedule every {hours} hours")
        while self.sch_rotate_logs:
            print("rotating logs")
            self.collect_data()
            t_sleep(60 * 60 * hours)

    def emit(self, message, level="INFO"):
        _msg = f"{datetime()} - {level:>10} - {self.name:>8}: {message}"
        print(_msg)
        with open(f"{self.path}/{self.filename}", "a") as f:
            f.write(_msg + "\n")

    def debug(self, message):
        self.emit(message, "DEBUG")

    def info(self, message):
        self.emit(message, "INFO")

    def warning(self, message):
        self.emit(message, "WARNING")

    def error(self, message):
        self.emit(message, "ERROR")

    def list(self):
        for item in listdir(self.path):
            print(item)

    def content(self, num:int=0):
        _file = f"{self.path}/{self.filename}"
        if num > 0:
            _file += f".{num}"
        with open(_file, 'r') as f:
            print(f.read())

    __call__ = info
