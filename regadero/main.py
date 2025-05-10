# main - telegram bot
from json import loads as json_loads
import ntptime

from logger import Logger

from gpio_manager import GpioManager
from wifi_manager import configure_wifi
from telegram_bot import TelegramBot
from utils import datetime


logger = Logger()

logger.info("getting settings")
SETTINGS = json_loads(open('settings.json', 'r').read())

gpm = GpioManager(SETTINGS["pins"])
if gpm:
    gpm.blink_led('red')

wlan = configure_wifi(SETTINGS['wifi'])
if wlan:
    gpm.blink_led('blue')

logger.info("configuring local time")
ntptime.host = "1.europe.pool.ntp.org"
ntptime.settime()
logger.info(f"  > time is {datetime.datetime()}")

tbot = TelegramBot(SETTINGS['telegram']['token'],
                   SETTINGS['telegram']['chat_id'])

