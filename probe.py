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
    # try:
    #     temp = -1
    #     temp = bmp.read()
    #     try:
    #         bmp.push(temp)
    #     except:
    #         print("Exception pushing temp to Adafruit.io")
    # except:
    #     print("Temp read exception, not pushing")

    try:
        temp = -1
        press = -1
        humidity = -1
        gas = -1
        temp, press, humidity, gas = bme.read()
        try:
            bme.push(temp, press, humidity, gas)
        except:
            print("Exception pushing env data to Adafruit.io")
    except:
        print("Env read exception, not pushing")


    try:
        lux = -1
        prox = -1
        lux, prox = ltr.read()
        try:
            ltr.push(lux,prox)
        except:
            print("Exception pushing lux to Adafruit.io")
    except:
        print("Lux read exception, not pushing")
        

#    oled.show(temp=temp, pressure=pressure, lux=lux)
    
    print(datetime.datetime.now(),
          " t=",temp,
          " p=",press,
          " h=",humidity,
          " g=",gas,
          " l=",lux)


    time.sleep(config.sleep_between_samples)
