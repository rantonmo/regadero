from machine import Pin

from microdot import Microdot, Response
from microdot.utemplate import Template


# from gpio_manager import GpioManager
from gpio_manager_small import blink
from utils import datetime, json_data
from wifi_manager import configure_wifi


settings = json_data(open('settings.json', 'r').read())

bled = Pin(2, Pin.OUT, value=0)

blink(bled, time=1.5)

wlan = configure_wifi(settings('wifi'))

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