#!/usr/bin/env python3

# Library with code to talk to sensors


from smbus2 import SMBus
from bmp280 import BMP280  # Temperature/pressure sensor
import ltr559              # Light/proximity sensor


class temp_sensor:
    def __init__(self, probe_id, aio):
        self.aio = aio
        bus = SMBus(1)
        self.temp_feed = self.aio.feeds(probe_id+'.temperature')
#        self.pressure_feed = self.aio.feeds(probe_id+'.pressure')
        self.bmp280 = BMP280(i2c_dev=bus)
    
    def read(self):
        tempc = self.bmp280.get_temperature()
        tempf = tempc * 9 / 5 + 32
        pressure = self.bmp280.get_pressure()
        return tempf, pressure
    
    def push(self, temp):       # Not including press
        self.aio.send(self.temp_feed.key, temp)
#        self.aio.send(self.pressure_feed.key, press)
        

class light_sensor:
    def __init__(self, probe_id, aio):
        self.aio = aio
        self.lux_feed = self.aio.feeds(probe_id+'.light')
    
    def read(self):
        lux = ltr559.get_lux()
        prox = ltr559.get_proximity()
        return lux, prox
    
    def push(self, lux):
        self.aio.send(self.lux_feed.key, lux)
