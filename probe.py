#!/usr/bin/env python3

import config

from Adafruit_IO import Client, Feed, RequestError

import time
import datetime

import libraries.sensors as sensors
import libraries.display as display


# Instantiate an Adafruit.IO object
aio = Client(config.adafruit_io_username, config.adafruit_io_key)
print(datetime.datetime.now(),"Adafruit.io initialized")

# Instantiate sensor objects
#bmp = sensors.temp_sensor(config.probe_id, aio)
#print(datetime.datetime.now(),"BMP280 sensor initialized")

bme = sensors.env_sensor(config.probe_id, aio)
print(datetime.datetime.now(),"BME680 sensor initialized")

ltr = sensors.light_sensor(config.probe_id, aio)
print(datetime.datetime.now(),"Light sensor initialized")


# Instantiate display
#oled = display.oled()

while True:
    try:
        bme.read()
        try:
            bme.push()
        except:
            print(datetime.datetime.now(),"EXCEPTION pushing env to Adafruit")
    except:
        print(datetime.datetime.now(),"Env read EXCEPTION, not pushing")


    try:
        ltr.read()
        try:
            ltr.push()
        except:
            print(datetime.datetime.now(),"EXCEPTION pushing light to Adafruit")
    except:
        print(datetime.datetime.now(),"Light read EXCEPTION, not pushing")
        

#    oled.show(temp=temp, pressure=pressure, lux=lux)
    
    print(datetime.datetime.now(),
          " t=",bme.temperature,
          " p=",bme.pressure,
          " h=",bme.humidity,
          " g=",bme.gas,
          " l=",ltr.light)

    time.sleep(config.sleep_between_samples)
