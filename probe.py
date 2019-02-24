#!/usr/bin/env python3

import config

from Adafruit_IO import Client, Feed, RequestError

import time
import datetime

import libraries.sensors as sensors
import libraries.display as display


# Instantiate an Adafruit.IO object
aio = Client(config.adafruit_io_username, config.adafruit_io_key)
print("Adafruit.io initialized")

# Instantiate sensor objects
bmp = sensors.temp_sensor(config.probe_id, aio)
print("BMP sensor initialized")

ltr = sensors.light_sensor(config.probe_id, aio)
print("Light sensor initialized")


# Instantiate display
#oled = display.oled()


while True:
    try:
        temp = -1
        temp = bmp.read()
        try:
            bmp.push(temp)
        except:
            print("Excepting pushing temp to Adafruit.io")
    except:
        print("Temp read exception, not pushing")

    try:
        lux = -1
        prox = -1
        lux, prox = ltr.read()
        try:
            ltr.push(lux)
        except:
            print("Excepting pushing lux to Adafruit.io")
    except:
        print("Lux read exception, not pushing")
        

#    oled.show(temp=temp, pressure=pressure, lux=lux)
    
    print(datetime.datetime.now()," temp=",temp," lux=",lux)


    time.sleep(config.sleep_between_samples)
