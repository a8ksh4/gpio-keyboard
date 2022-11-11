#!/usr/bin/env python

from gpiozero import Button
from time import sleep

# 24,  8, 27, 10, 11
# 23, 25,  7, 22,  9
buttons = (24, 8, 27, 10, 11, 23, 25, 7, 22, 9)

buttons = [Button(b) for b in buttons]

while True:
    for n, button in enumerate(buttons):
        if button.is_pressed:
            print(f'button {n} pressed')
    sleep(2)
