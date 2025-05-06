from json import loads as json_loads

from microdot import Microdot, Response
from microdot.utemplate import Template

from logger import Logger

from gpio_manager import GPIO_MANAGER
from wifi_manager import configure_wifi

logger = Logger()

logger.info("getting settings")
SETTINGS = json_loads(open('settings.json', 'r').read())

gpm = GPIO_MANAGER(SETTINGS["PINS"])
if gpm:
    gpm.blink_led('red', 3, 0.5)

wlan = configure_wifi(SETTINGS['wifi'])

if wlan:
    gpm.blink_led('blue')



app = Microdot()
Response.default_content_type = 'text/html'


@app.route('/', methods=['GET', 'POST'])
async def index(req):
    menu = "testing"
    if req.method == 'POST':
        led = req.form.get('led')
        action = req.form.get('action')
        if action == 'blink':
            gpm.blink_led(led)
        elif action == "on":
            gpm.led_on(led)
        elif action == "off":
            gpm.led_off(led)

    return Template('index.html').render(menu=menu)


@app.route('/page1')
async def index(req):
    return Template('page1.html').render(page='Page 1')


@app.route('/page2')
async def page2(req):

    return Template('page2.html').render(page='Page 2')

app.run(debug=True, port=8080)