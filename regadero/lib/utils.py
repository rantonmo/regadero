
from os import stat as os_stat, rename as f_rename, listdir

def f_exists(path) -> bool:
    try:
        if os_stat(path):
            return True
    except OSError:
        return False


class Logger():

    filename = None
    path = None
    name = None


    def __init__(self, filename="regadero.log", path="logs", name="root"):
        self.filename = filename
        self.path = path
        self.name = name
        if name == "root":
            self.rotate_old_logs()

        self.info("Logger initized")

    def rotate_old_logs(self):
        if f_exists(f"{self.path}/{self.filename}.1"):
            f_rename(f"{self.path}/{self.filename}.1", f"{self.path}/{self.filename}.2")

        if f_exists(f"{self.path}/{self.filename}"):
            f_rename(f"{self.path}/{self.filename}", f"{self.path}/{self.filename}.1")

        self.info("old logs has been rotated")


    def emit(self, message, level="INFO"):
        with open(f"{self.path}/{self.filename}", "a") as f:
            f.write(f"{level:>10} - {self.name:>8}: {message}\n")

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