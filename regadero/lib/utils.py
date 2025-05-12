
from json import loads as j_loads
from os import stat as os_stat
from time import localtime
def f_exists(path) -> bool:
    try:
        if os_stat(path):
            return True
    except OSError:
        return False

class datetime():

    @staticmethod
    def datetime():
        year, month, day, hour, minute, second, weekday, yearday = localtime()
        return f"{year}-{month}-{day}T{hour}:{minute}:{second}"

    @staticmethod
    def time():
        year, month, day, hour, minute, second, weekday, yearday = localtime()
        return f"{hour}:{minute}:{second}"

    @staticmethod
    def date():
        year, month, day, hour, minute, second, weekday, yearday = localtime()
        return f"{year}-{month}-{day}"

# this class is not running here in micropython
class json_data():

    data:dict = None

    def __init__(self, data:dict|str) -> None:
        if type(data) == str:
            self.data = j_loads(data)
        elif type(data) == dict:
            self.data = data
        else:
            raise NotImplementedError(f"type of data not supported: {type(data)}")

    def get(self, element:str, default:str=None):
        result = self.data.copy()
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

    __call__ = get