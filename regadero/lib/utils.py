
from os import stat as os_stat, rename as f_rename, listdir
from time import localtime
def f_exists(path) -> bool:
    try:
        if os_stat(path):
            return True
    except OSError:
        return False


# always Europe/Madrid for now
# ADJUST = {
#     "Europe/Madrid":{
#         "hours": 2,
#         "minutes": 00
#     }
# }

class datetime():

    @staticmethod
    def datetime():
        year, month, day, hour, minute, second, weekday, yearday = localtime()
        return f"{year}-{month}-{day}T{hour + 2}:{minute}:{second}"

    @staticmethod
    def time():
        year, month, day, hour, minute, second, weekday, yearday = localtime()
        return f"{hour + 2}:{minute}:{second}"

    @staticmethod
    def date():
        year, month, day, hour, minute, second, weekday, yearday = localtime()
        return f"{year}-{month}-{day}"
