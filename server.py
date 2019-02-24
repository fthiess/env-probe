#!/usr/bin/env python3

# Get outdoor temperature and upload samples to Adafruit.io

# Mountain View, CA = 2455920

from weather import Weather, Unit

weather = Weather(unit=Unit.FAHRENHEIT)

lookup = weather.lookup(2455920)
condition = lookup.condition

print(condition.text)