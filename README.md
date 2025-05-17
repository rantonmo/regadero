# regadero

A simple irrigation system.

## Firmware

[Download page](https://micropython.org/download/ESP32_GENERIC/)

**Clean up board:**

`esptool.py --port /dev/ttyUSB0 erase_flash`

**Upload firmware:**

`esptool.py --port /dev/ttyUSB0  --baud 460800 write_flash 0x1000 ~/Descargas/ESP32_GENERIC-20250415-v1.25.0.bin`


## Manage files
* **ampy:** `ampy -p /dev/tty.usbserial-1410 put max7219.py`
* **rshell** `rshell -p /dev/ttyUSB0 --editor vi --buffer-size=30`


_note:_ to edit files with rshell use the command `edit`, rshell will retreive the file and use the editor configured with the option `--editor`, and then update it:

**Install rshell** for micropython based board:
>`apt install  pyboard-rshell`

## Connection
`screen /dev/ttyUSB0 115200`

## Install dependencies - mip

[mip documentation](https://docs.micropython.org/en/latest/reference/packages.html)
[micropython-lib](https://github.com/micropython/micropython-lib)


**Example:**
```
>>> import mip
>>> mip.install("logging)
>>> mip.install("github:ThinkTransit/micropython-aioschedule")
```

## Web server

* [microdot](https://github.com/miguelgrinberg/microdot)
* [utemplate](https://github.com/pfalcon/utemplate)


# Schedule

https://github.com/rguillon/schedule

# Memory management - gc

* [memory collector - gc](https://docs.micropython.org/en/latest/library/gc.html)

```
>>> import gc
>>> gc.collect()
>>> gc.mem_free()
101696
>>> gc.mem_alloc()
24128
```

# flash space stats

https://forums.raspberrypi.com/viewtopic.php?t=345314