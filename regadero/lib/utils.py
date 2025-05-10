
from os import stat as os_stat
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

# this class is not running here in micropython
class json_data():
    data:dict = None

    def _init_(self, data:dict) -> None:
        self.data = data

    def get(self, element:str, default:str=''):
        result = self.data
        elements = element.split('.')
        for n, item in enumerate(elements):
            if item in result:
                result = result[item]
            elif item.isdigit():
                result = result[int(item)]
            elif '.'.join(elements[n:]) in result:
                # elements with . in key like {'buffer.size.bytes: 2000000 }
                return result['.'.join(elements[n:])]
            else:
                return default
        return result
    _call_ = get