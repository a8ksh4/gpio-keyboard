#!/usr/bin/env python3

import time
import board
import adafruit_adxl34x

i2c = board.I2C()  # uses board.SCL and board.SDA
acl = adafruit_adxl34x.ADXL345(i2c)

while True:
    print("Acceleration (m/s^2): X=%0.3f Y=%0.3f Z=%0.3f" % (acl.acceleration))
    #print("Acceleration (g's): X=%0.3f Y=%0.3f Z=%0.3f" % (acl.acceleration_g))
    #print("Temperature: %0.1f C" % acl.temperature)
    print("")
    time.sleep(0.5)