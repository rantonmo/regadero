
import gc
import _thread

from network import WLAN as N_WLAN, STA_IF as N_STA_IF
from os import stat as os_stat, statvfs as os_statvfs, uname as os_uname, listdir as os_listdir
from re import search as re_search
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

HELP_TEXT = """
* To show info: `system data` or `program data`
* To modify parameters: `set in program **ID** **PARAMETER** **VALUE**`
* To save program: `save program **ID**`
"""
def listen_to_commands(programs, system, bot):
    while True:
        for command in bot.get_commands():
            gc.collect()
            try:
                if re_search('system\s+data', command['text']):
                    bot.message_reaction(
                        command['chat'], command['message_id'])
                    bot.send_message(system.get_summary())
                elif re_search('programs?\s+(data|info)', command['text']):
                    bot.message_reaction(
                        command['chat'], command['message_id'])
                    text = f"*Programs at {datetime()}*\n"
                    for i, p in enumerate(programs):
                        text += f"_Program id {i}_:\n{p.get_summary()}\n"
                    bot.send_message(text)
                elif _m := re_search('sets+programs?\s+(\d+)\s+(\w+)\s+(\S+)', command['text']):
                    print(f" set in program {_m.group(1)} parameter: {_m.group(2)} value {_m.group(3)}")
                    if len(programs) < int(_m.group(0)):
                        _msg = programs[int(_m.group(1))].set_param(_m.group(2), _m.group(3))
                        bot.send_message(_msg)
                    else:
                        bot.send_message(f'wrong id for set param in program: {command['text']}')
                elif _m := re_search('save\s+program\s+(\d+)', command['text']):
                    if len(programs) < int(_m.group(0)):
                        programs[int(_m.group(0))].save()
                    else:
                        bot.send_message(f'wrong id for save program: {command['text']}')
                elif re_search('(hello|hola|hi|buenas)', command['text']):
                    bot.message_reaction(
                        command['chat'], command['message_id'], 'angel')
                    bot.send_message(f"Hi {command['username']} at {datetime()}")
                elif re_search('(fuck|idiota|jodete|cabr.?n|tonto|bobo|payaso)', command['text']):
                    bot.message_reaction(
                        command['chat'], command['message_id'], 'upset')
                    bot.send_message(f"What the fuck {command['username']}!!!")
                elif 'help' in command['text']:
                    bot.message_reaction(
                        command['chat'], command['message_id'], 'plased')
                    bot.send_message(HELP_TEXT)
                else:
                    bot.message_reaction(
                        command['chat'], command['message_id'], 'mmm')
                    bot.send_message(f"say what? -- '{command['text']}'")
            except OSError as exc:
                print("Error analizyng command %s: %s" % (command['text'], exc))

        t_sleep(20)

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

    def get_summary(self):
        return f"""
*System Status Summary*
    *Current datetime:* {datetime()}
    _Memory stats:_
    `usage: {self.memory['usage']} of {self.memory['total']}`

    _flash:_
    `Total flash: {self.flash['total']} free: {self.flash['free']}`

    _Wifi:_
    essid: `{self.wlan['essid']}` - ip: `{self.wlan['ip']}` rssi: `{self.wlan['rssi']}`
    """
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