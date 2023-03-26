#!/usr/bin/env python3



import lgpio as sbc
import time
import signal

def callback(chip, gpio, level, tick):
    print(f"{chip} {gpio} {level} {tick/1e9:.09f}")

# Define the GPIO pin to watch
chip = 0
PINS = (16, 21, 19, 25, 23, 
        20, 12, 26, 13, 24, 18)

print(dir(sbc))
sbc.exceptions = False

handle = sbc.gpiochip_open(chip)
for pin in PINS:
    sbc.gpio_claim_alert(handle, pin, sbc.BOTH_EDGES,lFlags=sbc.SET_BIAS_PULL_UP)
    sbc.gpio_set_debounce_micros(handle, pin, 100000)
    sbc.callback(handle, pin, sbc.BOTH_EDGES, callback)

sbc.exceptions = True
# Wait for the interrupt to happen
# while True:
#     time.sleep(10)
signal.pause()
