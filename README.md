# regadero

A simple irrigation system.

## Firmware

[Download page](https://micropython.org/download/ESP32_GENERIC/)

**Command to upload firmware:**

`esptool.py --port /dev/ttyUSB0  --baud 460800 write_flash 0x1000 ~/Descargas/ESP32_GENERIC-20250415-v1.25.0.bin`


## Manage files
* **ampy:** `ampy -p /dev/tty.usbserial-1410 put max7219.py`
* **rshell** `rshell -p /dev/ttyUSB0 --editor vi --buffer-size=30`

_note:_ to edit files with rshell use the command `edit`, rshell will retreive the file and use the editor configured with the option `--editor`, and then update it:


## Connection
`screen /dev/ttyUSB0 115200`


## Web server

* [microdot](https://github.com/miguelgrinberg/microdot)
* [utemplate](https://github.com/pfalcon/utemplate)


# Schedule

https://github.com/rguillon/schedule
