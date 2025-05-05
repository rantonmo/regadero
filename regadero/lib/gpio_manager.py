from utils import Logger
from machine import Pin
from time import sleep as t_sleep



class GPIO_MANAGER():
    leds = {}
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
            self.leds[led].off()  # always ends off

    def sound(self, times=4, sleep=0.5):  # default 2 seg -> 0.5 * 4
        self.logger.info(f"make sound: {times} - {sleep}", times, sleep)
        if self.buzz:
            for _i in range(0, times):
                self.buzz.toggle()
                t_sleep(sleep)
            self.buzz.off()  # always ends quiet