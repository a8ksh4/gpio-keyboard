#!/usr/bin/env python3

import time
import uinput

def main():
    events = (uinput.KEY_A, uinput.KEY_Z, uinput.KEY_LEFTCTRL, uinput.KEY_C)

    with uinput.Device(events) as device:
        time.sleep(1) 
        device.emit_click(uinput.KEY_A)
        device.emit_click(uinput.KEY_Z)
        device.emit(uinput.KEY_LEFTCTRL, 1, syn=True)
        time.sleep(0.1)
        device.emit_click(uinput.KEY_C, syn=True)
        time.sleep(0.1)
        device.emit(uinput.KEY_LEFTCTRL, syn=True)

if __name__ == "__main__":
    main()