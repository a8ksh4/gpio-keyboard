#!/usr/bin/env python3

import lgpio
from time import sleep
import signal

GPIO_PIN = 16

def callback(gpio, level, tick):
    if level == 0:
        print(f"GPIO {gpio} went low at tick {tick}")
    else:
        print(f"GPIO {gpio} went high at tick {tick}")

# open a connection to the pigpio daemon
pi = lgpio.pi()

# set the GPIO pin as an input
pi.set_mode(GPIO_PIN, lgpio.INPUT)

# set up a callback for when the pin changes state
cb = pi.callback(GPIO_PIN, lgpio.EITHER_EDGE, callback)

# configure the signal handler to pause the script when no events occur
def signal_handler(sig, frame):
    signal.pause()

signal.signal(signal.SIGINT, signal_handler)

# wait for events to occur
signal.pause()

# clean up the GPIO and callback
cb.cancel()
pi.stop()
# gpio = lgpio.gpiochip_open(0)

# BLOCKED_PINS = (0, 1) #, 7, 8)

# button_pins = (21, 20, 16, 12, 25, 24, 23, 18, 15, 14, 7, 8, 13, 19, 26)

# # button_pins = (16, 21, ?, 25, 23, 
# #                20, 12, ?, ? , 24,
# #                14, 15, 18)
# print(dir(lgpio))
# buttons = []
# # buttons = [Button(b) for b in button_pins]
# for p in button_pins:
#     if p in BLOCKED_PINS:
#         print('forbidden pin', p)
#         continue

#     print("init button", p)
#     #try:
#     butt = lgpio.gpiochip_get_line(gpio, p)
#     lgpio.gpio_claim_alert(gpio, butt)
#     lgpio.gpioSetAlertFunc(gpio, butt, lambda a, b, c: print('pressed', a, b, c))
#     buttons.append(butt)
#     #except:
#     #    print('error', p)
# print()

# pause()

# # while True:
# #     for n, button in enumerate(buttons):
# #         if button.is_pressed:
# #             print(f'button {n} pressed')
# #     sleep(2)
