from machine import Pin
from time import sleep as t_sleep

SP_TIME = {
    "sfast": 0.0625,
    "fast": 0.125,
    "normal": 0.25,
    "slow": 0.5,
    "sslow": 1
}

def blink(led:Pin, sleep:float=0.125, speed:str=None, time:int=1, off_value:int=1) -> None:
    """
    Blink a led connected to the Pin _led

    Parameters:
        * led: Pin connected to the led to blink
        * speed (str, optional): Speed to convert in time to be used as sleep. If speed is valid overwrite time
        * sleep (float, optional, default 0.125): time between switch on/off
        * time (intk optional, default 1): time to blink in seconds
        * off_value (init): value to put the pin off
    Return:
        None
    """
    if speed and speed in SP_TIME:
        sleep = SP_TIME['speed']
    led.value((off_value + 1) % 2)
    for i in range(time/sleep):
        led.toggle()
        t_sleep(sleep)
    led.value(off_value)