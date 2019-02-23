#!/usr/bin/env python3

import config

from Adafruit_IO import Client, Feed, RequestError

import time

import libraries/sensors
import libraries/display


# Instantiate an Adafruit.IO object
aio = Client(config.adafruit_io_username, config.adafruit_io_key)

# Instantiate sensor objects
bmp = sensors.temp_sensor(config.probe_id, aio)
ltr = sensors.light_sensor(config.probe_id, aio)

# Instantiate display
#oled = display.oled()


while True:
    temp, pressure = bmp.read()
    lux, prox = ltr.read()

#    oled.show(temp=temp, pressure=pressure, lux=lux)
    
    print("T: {:>5.2f}*F P: {:>8.2f}hPa L: {:>6.0f} Px: {:>5.0f}".format(temp, pressure, lux, prox))

    time.sleep(config.sleep_between_samples)
