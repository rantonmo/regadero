
import ntptime

from json import loads as json_loads
from machine import RTC

from microdot import Microdot, Response
from microdot.utemplate import Template

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
    gpm.blink_led('red', 3, 0.5)

wlan = configure_wifi(SETTINGS['wifi'])
if wlan and wlan.isconnected():
    gpm.blink_led('blue')

logger.info("configuring local time")
ntptime.host = "1.europe.pool.ntp.org"
ntptime.settime()
logger.info(f"  > time in UTC is {datetime.datetime()}")

logger.info("GMT adjustment (manual adjustment +02:00)")
rtc = RTC()

(Y, M, D, WD, h, m, s, ss) = rtc.datetime()
rtc.datetime((Y, M, D, WD, h + 2, m, s, ss))

logger.info(f"  > time adjusted is {datetime.datetime()}")


tbot = TelegramBot(SETTINGS['telegram']['token'],
                   SETTINGS['telegram']['chat_id'])

app = Microdot()
Response.default_content_type = 'text/html'

@app.route('/', methods=['GET', 'POST'])
async def index(req):
    if req.method == 'POST':
        led = req.form.get('led')
        action = req.form.get('action')
        if action == 'blink':
            gpm.blink_led(led)
        elif action == "on":
            gpm.led_on(led)
        elif action == "off":
            gpm.led_off(led)

    return Template('index.html').render(page="index")

@app.route('/program')
async def index(req):
    return Template('program.html').render(page='program')

@app.route('/wether')
async def index(req):
    return Template('wether.html').render(page='wether')

@app.route('/system')
async def page2(req):
    return Template('system.html').render(page='system')

app.run(debug=True, port=8080)