#!/usr/bin/env python3

import config

from smbus2 import SMBus
from bmp280 import BMP280  # Temperature/pressure sensor
import ltr559              # Light/proximity sensor

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106  # sh1107 is the same except 128x128

from PIL import ImageFont

from Adafruit_IO import Client, Feed, RequestError

import os
import time


class env_sensor:
    def __init__(self, probe_id, aio):
        bus = SMBus(1)
        self.feed = aio.feeds('temperature-' + probe_id)
        self.bmp280 = BMP280(i2c_dev=bus)
    
    def reading(self):
        tempc = self.bmp280.get_temperature()
        tempf = tempc * 9 / 5 + 32
        self.feed.send(self.feed.key, tempf)


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)

# Instantiate an Adafruit.IO object
aio = Client(config.adafruit_io_username, config.adafruit_io_key)

# Instantiate a env sensor object
bmp280 = env_sensor(config.probe_id, aio)

serial = i2c(port=1, address=0x3C)
device = sh1106(serial_interface=serial,
                width=128,
                height=128,    # Because default (64) is for sh1106
                rotate=2)      # Because of how display is mounted

font = make_font("DroidSansMono.ttf", 20)


pressure_feed = aio.feeds('pressure- '+ config.probe_id)
light_feed = aio.feeds('light-' + config.probe_id)


while True:
    temp = bmp280.reading()

    lux = ltr559.get_lux()
    prox = ltr559.get_proximity()

    with canvas(device) as draw:
        draw.text((0, 15), 'T {:>8.2f}'.format(temp), font=font, fill="white")
        draw.text((0, 50), 'P {:>8.2f}'.format(pressure), font=font, fill="white")
        draw.text((0, 85), 'L {:>8.2f}'.format(lux), font=font, fill="white")

    print("T: {:05.2f}*F P: {:08.2f}hPa L: {:08.2f} Px: {}".format(temp, pressure, lux, prox))

    aio.send(pressure_feed.key, pressure)
    aio.send(light_feed.key, lux)

    time.sleep(60)
