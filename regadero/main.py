from utils import Logger

from json import loads as json_loads

from gpio_manager import GPIO_MANAGER
from wifi_manager import configure_wifi


logger = Logger()

logger.info("this is a test - INFO")
logger.warning("this is a test - WARNING")
logger.error("this is a test - ERROR")


print("> Getting settings")
SETTINGS = json_loads(open('settings.json', 'r').read())

gpm = GPIO_MANAGER(SETTINGS["PINS"])

if gpm:
    gpm.blink_led('red', 3, 0.5)

wlan = configure_wifi(SETTINGS['wifi'])

if wlan:
    gpm.blink_led('blue')
