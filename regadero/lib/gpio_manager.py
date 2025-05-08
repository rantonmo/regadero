from logger import Logger
from machine import Pin
from time import sleep as t_sleep
import _thread

SP_TIME = {
    "fast": 0.15,
    "normal": 0.25,
    "slow": 0.5,
    "sslow": 1
}

class GpioManager():
    leds = {}
    _lock_led = {}
    buttons = {}
    buzz = None

    logger = None

    def __init__(self, _settings:dict) -> None:
        self.logger = Logger(name='gpio')

        for item in _settings:
            self.logger.info(f"{item} - {_settings[item]}")
            if _settings[item]["type"] == "buzzer":
                self.buzz = Pin(_settings[item]["pin"], Pin.OUT, value=0, drive=Pin.DRIVE_0)

            elif _settings[item]["type"] == "led":
                self.leds[item.lower()] = Pin(_settings[item]["pin"], Pin.OUT, value=0, drive=Pin.DRIVE_0)
                self.l_ock_led[item.lower()] = False

            elif _settings[item]["type"] == "button":
                self.buttons[item.lower()] = Pin(_settings[item]["pin"], Pin.IN, Pin.PULL_DOWN)

            else:
                self.logger.info(f"Error: unknow gpio type: {_settings[item]['type']}", )

    def list_leds(self):
        for item in self.leds.keys():
            print(item)

    def blink_led(self, led, times=6, sleep=0.25):  # default 3 seconds -> 0.25 * 12
        self.logger.info(f"blinking led {led} - {times} - {sleep}")
        if led in self.leds:
            for __i in range(0, times):
                self.leds[led].toggle()
                t_sleep(sleep)
            self.leds[led].off()


    def _blink_led(self, led, sleep=0.25):  # default 3 seconds -> 0.25 * 12
        self.logger.info(f"blinking led {led} - {sleep}")
        if led in self.leds:
            while self._lock_led[led]:
                self.leds[led].toggle()
                t_sleep(sleep)
            self.leds[led].off()

    def start_blink_led(self, led, speed="normal"):
        if not led in self._lock_led.keys():
            self.logger(f"led {led} not found!!! aborting...")
            return
        if self._lock_led[led]:
            self.logger(f"led {led} is locked!!! aborting...")
            return

        self.lock_led[led] = True
        self.logger(f"starting thread to blinking led {led}")
        return _thread.start_new_thread(self._blink_led, (led, SP_TIME[speed]))

    def stop_blink_led(self, led):
        self.logger.info(f"stoping blinking led {led}")
        if not led in self._lock_led.keys():
            self.logger(f"led {led} not found!!! aborting...")
        if not self._lock_led[led]:
            self.logger(f"led already stoped {led}!!!")
            return
        self._lock_led[led] = False

    def led_on(self, led):
        self.logger.info(f"set led {led} on")
        if led in self.leds:
            self.leds[led].on()
        else:
            self.logger.error(f"led {led} not configured")

    def led_off(self, led):
        self.logger.info(f"set led {led} ff")
        if led in self.leds:
            self.leds[led].off()
        else:
            self.logger.error(f"led {led} not configured")

    def sound(self, times=4, sleep=0.5):  # default 2 seg -> 0.5 * 4
        self.logger.info(f"make sound: {times} - {sleep}", times, sleep)
        if self.buzz:
            for _i in range(0, times):
                self.buzz.toggle()
                t_sleep(sleep)
            self.buzz.off()  # always ends quiet