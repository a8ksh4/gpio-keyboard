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
sbc.group_claim_input(handle, PINS, sbc.SET_BIAS_PULL_UP | sbc.SET_ACTIVE_LOW)
foo, mask = sbc.group_read(handle, PINS[0])
while True:
    foo, new_mask = sbc.group_read(handle, PINS[0])
    #same = mask ^ new_mask
    #pins = [n for n in range(32) if same & 2**n]
    print(mask, new_mask, mask==new_mask)
    pins = [n for n in range(32) if new_mask & 2**n]
    print(pins)
    time.sleep(1)