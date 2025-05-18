import ntptime
import gc
from time import sleep as t_sleep

from machine import RTC

from logger import Logger
from wifi_manager import configure_wifi
from gpio_manager import GpioManager
from telegram_bot import TelegramBot

from irrigation import Program

from utils import datetime, json_data, system_data

logger = Logger()

logger.info("schedule gc every day")
gc.threshold(24 * 60 * 60)

try:
    logger.info("reading main settings from file")
    settings = json_data(open('settings.json', 'r').read())
    logger.info("reading data file")
    data = json_data(open('data.json', 'r').read())
except Exception as exc:
    logger.error("Error reading settings or data: %s" % exc)

logger.info("configuring gpio")
gpm = GpioManager(settings("pins"))
if gpm:
    gpm.blink_led('red')

wlan = configure_wifi(settings('wifi'))
if wlan and wlan.isconnected():
    gpm.blink_led('blue')

logger.info("configuring local time")
ntptime.host = "1.europe.pool.ntp.org"
ntptime.settime()
logger.info(f"  > time in UTC is {datetime()}")

logger.info("GMT adjustment (manual adjustment +02:00)")
rtc = RTC()
(Y, M, D, WD, h, m, s, ss) = rtc.datetime()
rtc.datetime((Y, M, D, WD, h + 2, m, s, ss))
logger.info(f"  > time adjusted is {datetime()}")

logger.info("Initializing and starting system data collector")
sys_data = system_data()
sys_data.start()

logger.info("Initializing Telegram bot")
tbot = TelegramBot(settings('telegram.token'),
                   settings('telegram.chat_id'))

if tbot:
    gpm.blink_led('green')

programs = [Program(x, gpm, tbot) for x in data("programs")]

# for prog in programs:
#     prog.start()
#     t_sleep(0.1)
