#!/usr/bin/env python3

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

ADAFRUIT_IO_USERNAME = "fthiess"
ADAFRUIT_IO_KEY = "93c9681959fc4e828bb489c9028f4bab"


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)


bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

serial = i2c(port=1, address=0x3C)
device = sh1106(serial_interface=serial,
                width=128,
                height=128,    # Because default (64) is for sh1106
                rotate=2)      # Because of how display is mounted

font = make_font("DroidSansMono.ttf", 20)

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

temperature_feed = aio.feeds('temperature')
pressure_feed = aio.feeds('pressure')
light_feed = aio.feeds('light')


while True:
    tempc = bmp280.get_temperature()
    tempf = tempc * 9 / 5 + 32
    pressure = bmp280.get_pressure()

    lux = ltr559.get_lux()
#    prox = ltr559.get_proximity()

    with canvas(device) as draw:
        draw.text((0, 15), 'T {:>8.2f}'.format(tempf), font=font, fill="white")
        draw.text((0, 50), 'P {:>8.2f}'.format(pressure), font=font, fill="white")
        draw.text((0, 85), 'L {:>8.2f}'.format(lux), font=font, fill="white")

    print("T: {:05.2f}*F P: {:08.2f}hPa L: {:08.2f}".format(tempf, pressure, lux))

    aio.send(temperature_feed.key, tempf)
    aio.send(pressure_feed.key, pressure)
    aio.send(light_feed.key, lux)

    time.sleep(60)
