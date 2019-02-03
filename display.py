#!/usr/bin/env python3

# Library for SH1107 OLED display

import config

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106  # sh1107 is the same except 128x128

from PIL import ImageFont

import os


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)


class oled:
    def __init__(self):
        serial = i2c(port=1, address=0x3C)
        self.device = sh1106(serial_interface=serial,
                        width=128,
                        height=128,    # Because default (64) is for sh1106
                        rotate=2)      # Because of how display is mounted
        self.font = make_font("DroidSansMono.ttf", 20)

    def show(self, temp, pressure, lux):
        with canvas(self.device) as draw:
            draw.text((0, 15), 'T {:>8.2f}'.format(temp), font=self.font, fill="white")
            draw.text((0, 50), 'P {:>8.2f}'.format(pressure), font=self.font, fill="white")
            draw.text((0, 85), 'L {:>6.0f}'.format(lux), font=self.font, fill="white")
                            
