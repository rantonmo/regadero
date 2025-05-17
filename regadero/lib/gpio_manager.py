from logger import Logger
from machine import Pin
from time import sleep as t_sleep
import _thread

SP_TIME = {
    "sfast": 0.0625,
    "fast": 0.125,
    "normal": 0.25,
    "slow": 0.5,
    "sslow": 1
}

# simple blink function - usefull for esp8266
def blink(led:Pin, sleep:float=0.125, speed:str=None, time:int=1, off_value:int=0) -> None:
    """
    Blink a led connected to the Pin _led

    Parameters:
        * led: Pin connected to the led to blink
        * speed (str, optional): Speed to convert in time to be used as sleep. If speed is valid overwrite time
        * sleep (float, optional, default 0.125): time between switch on/off
        * time (intk optional, default 1): time to blink in seconds
        * off_value (init): value to put the pin off
    Return:
        None
    """
    if speed and speed in SP_TIME:
        sleep = SP_TIME['speed']
    led.value((off_value + 1) % 2)
    for i in range(time/sleep):
        led.toggle()
        t_sleep(sleep)
    led.value(off_value)

class GpioManager():
    leds = {}
    _lock_led = {}
    buttons = {}
    switchs = {}
    buzz = None

    logger = None

    def __init__(self, _settings:dict) -> None:
        self.logger = Logger(name='gpio')

        for item in _settings:
            self.logger.info(f"{item} - {_settings[item]}")
            if _settings[item]["type"] == "buzzer":
                self.buzz = Pin(_settings[item]["pin"], Pin.OUT, value=0, drive=Pin.DRIVE_0)

            elif _settings[item]["type"] == "led":
                if 'drive' in _settings[item]:
                    if type(_settings[item]["drive"]) == int and _settings[item]["drive"] < 4:
                        _drive = _settings[item]["drive"]
                    else:
                        self.logger.warning(f" - wrong drive value in settings for led {item}: {_settings[item]["drive"]}")
                else:
                    _drive = Pin.DRIVE_0
                self.leds[item.lower()] = Pin(_settings[item]["pin"], Pin.OUT, value=0, drive=_drive)
                self._lock_led[item.lower()] = False

            elif _settings[item]["type"] == "button":
                self.buttons[item.lower()] = Pin(_settings[item]["pin"], Pin.IN, Pin.PULL_DOWN)
            elif _settings[item]["type"] == "switch":
                self.switchs[item.lower()] = Pin(_settings[item]["pin"], Pin.OUT, value=0)
            else:
                self.logger.info(f"Error: unknow gpio type: {_settings[item]['type']}", )

    def list_leds(self):
        for item in self.leds.keys():
            print(item)

    def blink_led(self, led, speed:str=None, time=1.5, sleep=0.25, off_value=0):

        self.logger.info(f"blinking led {off_value} - {led} - {speed} - {sleep} - {time}")
        if led in self.leds:
            self.leds[led].value((off_value + 1) % 2)

            if speed and speed in SP_TIME:
                sleep = SP_TIME['speed']

            for __i in range(0, time/sleep):
                self.leds[led].toggle()
                t_sleep(sleep)
            self.leds[led].value(off_value)
        else:
            self.logger.error(f"led {led} not found or not configured. Aborting...")

    def blink_led_until_lock(self, led, speed:str=None, sleep=0.25, off_value=0):
        self.logger.info(f"blinking led {off_value} - {led} - {speed} - {sleep}")

        if led in self.leds:
            # set init value
            self.leds[led].value(off_value)

            if speed and speed in SP_TIME:
                sleep = SP_TIME['speed']

            while self._lock_led[led]:
                self.leds[led].toggle()
                t_sleep(sleep)
            # end with off - switch init value
            self.leds[led].value((off_value + 1) % 2)
        else:
            self.logger.error(f"led {led} not found or not configured. Aborting...")

    def start_blink_led(self, led, speed="normal"):
        if not led in self._lock_led.keys():
            self.logger.info(f"led {led} not found!!! aborting...")
            return
        if self._lock_led[led]:
            self.logger.info(f"led {led} is locked!!! aborting...")
            return

        self._lock_led[led] = True
        self.logger.info(f"starting thread to blinking led {led} - {speed} ({SP_TIME[speed]})")
        return _thread.start_new_thread(self.blink_led_until_lock, (led, SP_TIME[speed]))

    def stop_blink_led(self, led):
        self.logger.info(f"stoping blinking led {led}")
        if not led in self._lock_led.keys():
            self.logger.info(f"led {led} not found!!! aborting...")
        if not self._lock_led[led]:
            self.logger.info(f"led already stoped {led}!!!")
            return
        self._lock_led[led] = False

    def led_toggle(self, led):
        if not led:
            self.logger.error("toggle needs a led to be toggled. Aborting")
        self.logger.info(f"toggle led {led}")
        if led in self.leds:
            self.leds[led].toggle()
        else:
            self.logger.error(f"led {led} not configured")

    def led_on(self, led):
        self.logger.info(f"set led {led} on")
        if led in self.leds:
            self.leds[led].on()
        else:
            self.logger.error(f"led {led} not configured")

    def led_off(self, led):
        self.logger.info(f"set led {led} off")
        if led in self.leds:
            self.leds[led].off()
        else:
            self.logger.error(f"led {led} not configured")

    def sound(self, sleep=0.5, time=2) -> None:
        """
        Make sound with a buzzer
        Parameters:
            * sleep (float, default 0.5): time between switch on/off
            * time (int, default 2): seconds to make sound
        Return:
            None
        """
        self.logger.info(f"make sound: {sleep} - {time}")
        if self.buzz:
            for _i in range(0, time/sleep):
                self.buzz.toggle()
                t_sleep(sleep)
            self.buzz.off()  # always ends quiet

    def blink(self, led:str, sleep:float=0.125, speed:str=None, time:int=1, led_init=0) -> None:
        """
        Blink a led connected to the Pin _led

        Parameters:
            * led (str): pin name
            * speed (str, optional): Speed to convert in time to be used as sleep. If speed is valid overwrite time
            * sleep (float, optional, default 0.125): time between switch on/off
            * time (intk optional, default 1): time to blink in seconds
        Return:
            None
        """
        led.value(led_init)

        if speed and speed in SP_TIME:
            sleep = SP_TIME['speed']

        for i in range(time/sleep):
            led.toggle()
            t_sleep(sleep)

    on = led_on
    off = led_off
    __call__ = led_toggle