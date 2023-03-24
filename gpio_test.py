#!/usr/bin/env python3

from gpiozero import Button
from time import sleep
from signal import pause

BLOCKED_PINS = (0, 1) #, 7, 8)

button_pins = (21, 20, 16, 12, 25, 24, 23, 18, 15, 14, 7, 8, 13, 19, 26)

# button_pins = (16, 21, ?, 25, 23, 
#                20, 12, ?, ? , 24,
#                14, 15, 18)

buttons = []
# buttons = [Button(b) for b in button_pins]
for p in button_pins:
    if p in BLOCKED_PINS:
        print('forbidden pin', p)
        continue

    print("init button", p)
    try:
        butt = Button(p, bounce_time = 0.1)
        butt.when_pressed = lambda b: print('pressed', b.pin)
        #butt.when_released = lambda b: print('released', b.pin)
        buttons.append(butt)
    except:
        print('error', p)
print()

pause()

# while True:
#     for n, button in enumerate(buttons):
#         if button.is_pressed:
#             print(f'button {n} pressed')
#     sleep(2)
