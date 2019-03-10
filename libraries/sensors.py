#!/usr/bin/env python3

# Library with code to talk to sensors
from smbus2 import SMBus
from bmp280 import BMP280  # Temperature/pressure sensor
import bme680              # Temp, pressure, humidity, VOC sensor
import ltr559              # Light/proximity sensor

import config

class temp_sensor:
    def __init__(self, probe_id, aio):
        self.aio = aio
        bus = SMBus(1)
        self.temp_feed = self.aio.feeds(probe_id+'.temperature')
        self.pressure_feed = self.aio.feeds(probe_id+'.pressure')
        self.bmp280 = BMP280(i2c_dev=bus)
    
    def read(self):
        tempc = self.bmp280.get_temperature()
        tempf = tempc * 9 / 5 + 32
        pressure = self.bmp280.get_pressure()
        return tempf
    
    def push(self, temp):
        self.aio.send(self.temp_feed.key, temp)
        self.aio.send(self.pressure_feed.key, press)


class env_sensor:
    def __init__(self, probe_id, aio):
        self.aio = aio
        self.temp_feed = self.aio.feeds(probe_id+'.temperature')
        self.humid_feed = self.aio.feeds(probe_id+'.humidity')
        self.gas_feed = self.aio.feeds(probe_id+'.gas')
        self.pressure_feed = self.aio.feeds(probe_id+'.pressure')

        self.bme680 = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        
        self.bme680.set_humidity_oversample(bme680.OS_2X)
        self.bme680.set_pressure_oversample(bme680.OS_4X)
        self.bme680.set_temperature_oversample(bme680.OS_8X)
        self.bme680.set_filter(bme680.FILTER_SIZE_3)

        self.bme680.set_gas_status(bme680.ENABLE_GAS_MEAS)
        self.bme680.set_gas_heater_temperature(320)
        self.bme680.set_gas_heater_duration(150)
        self.bme680.select_gas_heater_profile(0)
         
    
    def read(self):
        self.temperature = -1
        self.pressure = -1
        self.humidity = -1
        self.gas = -1
         
        if self.bme680.get_sensor_data():
            tempc = self.bme680.data.temperature         # Celsius
            self.temperature = tempc * 9 / 5 + 32 + config.temperature_offset
 
            self.pressure = self.bme680.data.pressure + config.pressure_offset        # hectoPascals
            self.humidity = self.bme680.data.humidity + config.humidity_offset        # % relative
         
            if self.bme680.data.heat_stable:
                 self.gas = self.bme680.data.gas_resistance + config.gas_offset   # Ohms
            
    def push(self):
        if self.temperature != -1:
            self.aio.send(self.temp_feed.key, self.temperature)
        if self.humidity != -1:
            self.aio.send(self.humid_feed.key, self.humidity)
        if self.pressure != -1:
            self.aio.send(self.pressure_feed.key, self.pressure)
        if self.gas != -1:
            self.aio.send(self.gas_feed.key, self.gas)


class light_sensor:
    def __init__(self, probe_id, aio):
        self.aio = aio
        self.lux_feed = self.aio.feeds(probe_id+'.light')
    
    def read(self):
        self.light = ltr559.get_lux() + config.light_offset
        self.proximity = ltr559.get_proximity() + config.proximity_offset
    
    def push(self):
        if self.light != -1:
            self.aio.send(self.lux_feed.key, self.light)
