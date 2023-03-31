#!/usr/bin/env python3

import lgpio as sbc
import time
import signal

def callback(chip, gpio, level, tick):
    print(f"{chip} {gpio} {level} {tick/1e9:.09f}")

def checkEncoder(solo, last, pins):
    active_pin = None
    if last is None:
        last = pins
        return solo, last, active_pin
    
    if solo is None and len(pins) == 1:
        solo = pins[0]
        
    if solo is None and len(pins) == 2:
        last = pins
        return solo, last, active_pin
    
    if last == pins:
        return solo, last, active_pin
    
    # Something is happening!
    print('last', last, 'pins', pins, 'solo', solo)
    
    if last == []:
        #encoder activation
        if len(pins) == 2: 
            print('solo', pins, pins[0], solo)
            active_pin = [p for p in pins if p != solo][0]
        else:
            print('not solo', pins, pins[0])
            active_pin = pins[0]
        last = pins
    else:
        last = pins
        
    if active_pin is not None:
        print(f"    Encoder activated on pin {active_pin}")

    return solo, last, active_pin

# Define the GPIO pin to watch
chip = 0
PINS = (14, 15)
GPIO_PINS = (14, 15)

print(dir(sbc))
sbc.exceptions = False

handle = sbc.gpiochip_open(chip)
sbc.group_claim_input(handle, PINS, sbc.SET_BIAS_PULL_UP | sbc.SET_ACTIVE_LOW)
last = None
solo = None
foo, mask = None, None
while True:
    foo, new_mask = sbc.group_read(handle, PINS[0])
    if new_mask == mask and mask is not None:
        continue
    mask = new_mask
    pins = [n for n in range(32) if mask & 2**n]
    print(int(time.time_ns() / 1000000), pins)
    
    solo, last, active_pin = checkEncoder(solo, last, pins)
        
    if active_pin is not None:
        print(f"    Encoder activated on pin {active_pin}")

            
            
    