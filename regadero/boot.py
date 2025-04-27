# boot file of the regadero project
from json import loads as json_loads
from machine import Pin
from network import WLAN as N_WLAN, STA_IF as N_STA_IF
from time import sleep as time_sleep

print("Initializing board...")

print("> Getting settings")
SETTINGS = json_loads(open('settings.json', 'r').read())

print("> Configure pins")
red = Pin(SETTINGS["pins"]["RED"], Pin.OUT, value=0, drive=Pin.DRIVE_0)
green = Pin(SETTINGS["pins"]["GREEN"], Pin.OUT, value=0, drive=Pin.DRIVE_0)
blue = Pin(SETTINGS["pins"]["BLUE"], Pin.OUT, value=0, drive=Pin.DRIVE_0)

buzz = Pin(SETTINGS["pins"]["BUZZ"], Pin.OUT, value=0, drive=Pin.DRIVE_0)

left = Pin(SETTINGS["pins"]["LEFT"], Pin.IN, Pin.PULL_DOWN)
right = Pin(SETTINGS["pins"]["RIGHT"], Pin.IN, Pin.PULL_DOWN)

print("> Configuring wifi")
wlan = N_WLAN(N_STA_IF)
wlan.active(True)
wlan.config(dhcp_hostname=SETTINGS['wifi']['hostname'])
wlan.connect(SETTINGS['wifi']['essid'], SETTINGS['wifi']['key'])

maxtry = 120
__i = 0

while not wlan.isconnected() or __i < maxtry:
    print("   (%3s/%s))connecting to wifi %s" % SETTINGS['wifi']['essid'])
    time_sleep(0.5)
if not wlan.isconnected():
    raise RuntimeError("Error connecting to the wifi %s" % SETTINGS['wifi']['essid'])

print("Connected to wifi: %s - rssi: %s - channel: %s" % (wlan.config('essid'), wlan.status('rssi'), wlan.config('channel')))