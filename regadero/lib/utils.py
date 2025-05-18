
import gc
import _thread

from network import WLAN as N_WLAN, STA_IF as N_STA_IF
from os import stat as os_stat, statvfs as os_statvfs, uname as os_uname, listdir as os_listdir
from time import localtime as t_localtime, sleep as t_sleep

from json import loads as j_loads

def f_exists(path) -> bool:
    try:
        if os_stat(path):
            return True
    except OSError:
        return False

def isdir(path) -> bool:
    try:
        if type(os_listdir(path)) == list:
            return True
    except:
        return False

def datetime(custom_time=None):
    year, month, day, hour, minute, second, weekday, yearday = t_localtime(custom_time)
    return f"{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}"

def time(custom_time=None):
    year, month, day, hour, minute, second, weekday, yearday = t_localtime(custom_time)
    return f"{hour:02d}:{minute:02d}:{second:02d}"

def date(custom_time=None):
    year, month, day, hour, minute, second, weekday, yearday = t_localtime(custom_time)
    return f"{year}-{month:02d}-{day:02d}"

# this class is not running here in micropython
class json_data():

    data:dict = None

    def __init__(self, data:dict|str) -> None:
        if type(data) == str:
            self.data = j_loads(data)
        elif type(data) == dict:
            self.data = data
        else:
            raise NotImplementedError(
                f"type of data not supported: {type(data)}")

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

class system_data():

    enabled = True

    system = None
    memory = None
    flash = None
    wlan = None

    def __init__(self):
        uname = os_uname()
        self.system = {  # unmutable data
            "sysname": uname[0],
            "nodename": uname[1],
            "release": uname[2],
            "machine": uname[4]
        }

        self.collect_data()

    def collect_data(self):
        self.get_memory_stats()
        self.get_flash_stats()
        self.get_wlan_stats()

    def get_wlan_stats(self):
        wlan = N_WLAN(N_STA_IF)
        mac = wlan.config('mac')

        if not wlan.isconnected():
            self.wlan =  {
                "essid": wlan.config('essid'),
                "ip": wlan.ifconfig()[0],
                "mac": f"{mac[0]:02x}:{mac[1]:02x}:{mac[2]:02x}:{mac[3]:02x}:{mac[4]:02x}",
                "rssi": '',
                "channel": '',
                "hostname": '',
                "status": "not connected"
            }
            return

        self.wlan = {
            "essid": wlan.config('essid'),
            "ip": wlan.ifconfig()[0],
            "mac": f"{mac[0]:02x}:{mac[1]:02x}:{mac[2]:02x}:{mac[3]:02x}:{mac[4]:02x}",
            "rssi": wlan.status('rssi'),
            "channel": wlan.config('channel'),
            "hostname": wlan.config('hostname'),
            "status": wlan.status()
        }

    def get_flash_stats(self):
        stats = os_statvfs('/')

        self.flash = {
            "total": (stats[1] * stats[2]) / (1024 * 1024),
            "free": (stats[0] * stats[3]) / (1024 * 1024)
        }

    def get_memory_stats(self):
        collected = gc.collect()
        free = gc.mem_free()  # bytes
        alloc = gc.mem_alloc()  # bytes

        total = free +  alloc
        usage = (free + alloc) / (100 * alloc)

        self.memory = {
            "total": total / 1024,
            "usage": usage / 1024,
            "free": free / 1024,
            "used": alloc / 1024,
            "collected": collected
        }

    def start(self):
        self.enabled = True
        _thread.start_new_thread(self._start_collecting_stats, ())

    def stop(self):
        self.enabled = False

    def _start_collecting_stats(self, minutes=30):
        while self.enabled:
            print("collecting system data")
            self.collect_data()
            t_sleep(60 * minutes)