#!/usr/bin/env python3

import config

# from smbus2 import SMBus
# from bmp280 import BMP280  # Temperature/pressure sensor
# import ltr559              # Light/proximity sensor

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106  # sh1107 is the same except 128x128

from PIL import ImageFont

from Adafruit_IO import Client, Feed, RequestError

import os
import time

import sensors


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)

# Instantiate an Adafruit.IO object
aio = Client(config.adafruit_io_username, config.adafruit_io_key)

# Instantiate sensor objects
bmp = sensors.temp_sensor(config.probe_id, aio)
ltr = sensors.light_sensor(config.probe_id, aio)

serial = i2c(port=1, address=0x3C)
device = sh1106(serial_interface=serial,
                width=128,
                height=128,    # Because default (64) is for sh1106
                rotate=2)      # Because of how display is mounted

font = make_font("DroidSansMono.ttf", 20)


while True:
    temp, pressure = bmp.reading()
    lux, prox = ltr.reading()

    with canvas(device) as draw:
        draw.text((0, 15), 'T {:>8.2f}'.format(temp), font=font, fill="white")
        draw.text((0, 50), 'P {:>8.2f}'.format(pressure), font=font, fill="white")
        draw.text((0, 85), 'L {:>8.2f}'.format(lux), font=font, fill="white")

    print("T: {:05.2f}*F P: {:08.2f}hPa L: {:08.2f} Px: {}".format(temp, pressure, lux, prox))

    time.sleep(10)
