import ntptime

from json import loads as json_loads
from machine import RTC, Pin

from logger import Logger
from wifi_manager import configure_wifi
from gpio_manager_small import blink
from telegram_bot import TelegramBot

from utils import datetime

SETTINGS = json_loads(open('settings.json', 'r').read())

logger = Logger()

logger.info("configuring onboard led")
bled = Pin(2, Pin.OUT, drive=Pin.DRIVE_0)


wlan = configure_wifi(SETTINGS['wifi'])
if wlan.isconnected():
    blink(bled)


logger.info("configuring local time")
ntptime.host = "1.europe.pool.ntp.org"
ntptime.settime()
logger.info(f"  > time in UTC is {datetime.datetime()}")

logger.info("GMT adjustment (manual adjustment +02:00)")
rtc = RTC()
(Y, M, D, WD, h, m, s, ss) = rtc.datetime()
rtc.datetime((Y, M, D, WD, h + 2, m, s, ss))
logger.info(f"  > time adjusted is {datetime.datetime()}")

logger.info("Initializing Telegram bot")
tbot = TelegramBot(SETTINGS['telegram']['token'],
                #    SETTINGS['telegram']['group_chat_id'])
                   SETTINGS['telegram']['chat_id'])
if tbot:
    blink(bled)

tbot.send_message("regadero (testing) has been initialized")


