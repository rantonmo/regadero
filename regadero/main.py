from json import loads as json_loads
from machine import Pin
from time import sleep as time_sleep

print("> Getting settings")
SETTINGS = json_loads(open('settings.json', 'r').read())

print("> Configure pins")
red = Pin(SETTINGS["pins"]["RED"], Pin.OUT, value=0, drive=Pin.DRIVE_0)
green = Pin(SETTINGS["pins"]["GREEN"], Pin.OUT, value=0, drive=Pin.DRIVE_0)
blue = Pin(SETTINGS["pins"]["BLUE"], Pin.OUT, value=0, drive=Pin.DRIVE_0)

buzz = Pin(SETTINGS["pins"]["BUZZ"], Pin.OUT, value=0, drive=Pin.DRIVE_0)

left = Pin(SETTINGS["pins"]["LEFT"], Pin.IN, Pin.PULL_DOWN)
right = Pin(SETTINGS["pins"]["RIGHT"], Pin.IN, Pin.PULL_DOWN)


while True:
    green.on()
    time_sleep(0.5)
    green.off()