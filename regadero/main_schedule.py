import ntptime
from time import sleep as t_sleep

from machine import RTC

from logger import Logger
from wifi_manager import configure_wifi
from gpio_manager import GpioManager
from telegram_bot import TelegramBot

from irrigation_scheduler import Program

from utils import datetime, json_data

logger = Logger()

try:
    logger.info("reading main settings from file")
    settings = json_data(open('settings.json', 'r').read())
    logger.info("reading data file")
    data = json_data(open('data.json', 'r').read())
except Exception as exc:
    logger.error("Error reading settings or data: %s" % exc)

logger.info("configuring onboard led")
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

logger.info("Initializing Telegram bot")
tbot = TelegramBot(settings('telegram.token'),
                   settings('telegram.chat_id'))

if tbot:
    gpm.blink_led('green')

tbot.send_message("regadero (testing) has been initialized", notify=False)
programs = [Program(x) for x in data("programs")]

for prog in programs:
    prog.start()
    t_sleep(0.1)

# logger.info("Configuring program %s" % data("programs.0"))
# prog = Program(data("programs.0"))
# logger.info(f" program {prog.name} will be executed at {datetime(prog.next_run_datetime)}")
# prog.start_program()
