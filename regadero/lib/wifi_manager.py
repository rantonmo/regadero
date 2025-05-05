from utils import Logger

from network import WLAN as N_WLAN, STA_IF as N_STA_IF
from time import sleep as t_sleep

logfile = "logs/regadero.log"

def configure_wifi(wificonfig:dict, maxtry=40) -> N_WLAN:

    logger = Logger(name="wifi")

    wlan = N_WLAN(N_STA_IF)
    wlan.active(True)
    if wificonfig.get('hostname'):
        logger.info(f"configuring hostname: {wificonfig['hostname']}")
        wlan.config(dhcp_hostname=wificonfig['hostname'])
    wlan.connect(wificonfig['essid'], wificonfig['key'])
    __i = 0

    while __i < maxtry:
        if wlan.isconnected():
            break
        logger.info("  [%3s/%s] connecting to wifi %s - %s" % (__i, maxtry, wificonfig['essid'], wlan.isconnected()))
        t_sleep(0.5)
        __i += 1

    if wlan.isconnected():
        logger.info(f"wlan connected: {wlan.ifconfig()}")
        return wlan

    logger.error(f"Error connecting to wlan {wificonfig['essid']} - {wlan.isconnected()} - {wlan.ifconfig()}")
