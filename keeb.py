#!/usr/bin/env python3

from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero.pins.rpigpio import RPiGPIOFactory
from gpiozero import Button
import threading as th
import time
from keymap import LAYERS, CHORDS, PINS
from keys import SHIFTED #, CTRLED, CODES
import os
import collections
import subprocess as sp
import uinput
from uinput_translate import UINPUT_ACTIVATE, UINPUT_TRANSLATE
from signal import pause

#PINS = [Pin(p, Pin.IN, Pin.PULL_UP) for p in PINS]
#PINS = [Button(p) for p in PINS]

#HOLD_TIME = 500
#LAYER_HOLDTIME = 300
#CHORD_WAITTIME = 500
HOLDTIME = 250
# ONESHOT_TIMEOUT = 500
BASE_LAYER = 0
TICKER = 0
EVENTS = []
PENDING_BUTTONS = set()
OS_SHIFT_PENDING = False
OS_CTRL_PENDING = False
TIMER = None
DEBUG = False
DELAYED_INPUT = [] # interface for other tools to ask for something to be typed.
BUTTONS_PRESSED = []


# Strategery
# First keypress starts the process
# Passing layer hold time transitions layer if it's a layer key
#    layer transition stays until layer key is released
# chord time starts when first key is pressed (or reset when layer shift is triggered)
# 

def printd(foo):
    global DEBUG
    if DEBUG:
        print(foo) 


def get_output_key(buttons, layer, tap):
    # global PINS
    global LAYERS
    global CHORDS
    #print('foo buttons:', buttons, 'layer:', layer, 'tap:', tap)

    mapped_buttons = [LAYERS[layer][b] for b in buttons]
    if len(mapped_buttons) > 1 or tap:
        # convert any hold-tap layer keys to just the (tap) key
        mapped_buttons = [b if isinstance(b, str) else b[1] for b in mapped_buttons]
        mapped_buttons = tuple(sorted(mapped_buttons))
        if len(mapped_buttons) > 1:
            result = CHORDS.get(mapped_buttons, None)
            #print("RESULT:", result)
            if isinstance(result, str):
                result = result, None
            if result is None:
                result = None, None
        else:
            result = mapped_buttons[0], None

    else:
        if isinstance(mapped_buttons[0], str):
            result = mapped_buttons[0], None
        else:
            result = None, mapped_buttons[0][0]
    
    #print(f'get output key: {buttons}, {layer}, {tap}, {result}')
    return result

def time_ms():
    return int(time.time_ns() / 1000000)


def event_handler(active_button):
    #print('FOO', foo)
    global TICKER  
    global HOLDTIME
    global BASE_LAYER
    global EVENTS
    global PENDING_BUTTONS
    global PINS
    global OS_SHIFT_PENDING
    global OS_CTRL_PENDING
    global DELAYED_INPUT
    global BUTTONS_PRESSED

    # clock = time.ticks_ms()
    clock = time_ms()

    current_layer = [BASE_LAYER,] + [e['layer'] for e in EVENTS if e['layer']]
    current_layer = current_layer[-1]

    active_pin = [n for n, p in enumerate(PINS) if p == active_button.pin.number][0]
    print(active_pin)
    if active_button.is_pressed:
        BUTTONS_PRESSED.append(active_pin)
    else:
        BUTTONS_PRESSED.remove(active_pin)

    # # buttons_pressed = [n for n, p  in enumerate(PINS) if not p.value()]
    # buttons_pressed = [n for n, p  in enumerate(PINS) if p.is_pressed]
    # if buttons_pressed:
    #     pass

    # Remove events whos buttons are no longer pressed.
    for event in EVENTS:
        still_pressed = [b for b in event['buttons'] if b in BUTTONS_PRESSED]
        if not still_pressed:
            EVENTS.remove(event)

    # Remove buttons from buttons_pressed if associated with an event
    all_event_butons = sum([e['buttons'] for e in EVENTS], [])
    #print('all event buttons:', all_event_butons)
    buttons_pressed = [b for b in BUTTONS_PRESSED if b not in all_event_butons]
    # TODO: mark events inactive if not all of their original buttons are still pressed.

    # Move buttons_pressed to pending
    PENDING_BUTTONS.update(buttons_pressed)
    # At this point, pending buttons is only buttons pressed that have not been associated with an event. 

    if PENDING_BUTTONS:
        if not TICKER:
            TICKER = clock
        print('Pending:', PENDING_BUTTONS)

        # Check conditions for new event - Keys starting to be released or hold_time exceeded
        # TODO: maybe separate hold times for layer stuff vs chords. 
        if ( len(PENDING_BUTTONS) > len(buttons_pressed) 
                or clock - TICKER > HOLDTIME ):
            tap =  clock - TICKER < HOLDTIME

            printd(f'{(len(PENDING_BUTTONS), len(buttons_pressed), clock, TICKER, clock-TICKER)}')
            print(PENDING_BUTTONS, current_layer, tap)
            output_key, new_layer = get_output_key(PENDING_BUTTONS, current_layer, tap)

            print(output_key, new_layer)
            if output_key == '_set_base':
                BASE_LAYER = new_layer
                output_key, new_layer = None, None

            if output_key == '_os_shft':
                OS_SHIFT_PENDING = True
                output_key = None

            if output_key == '_os_ctrl':
                OS_CTRL_PENDING = True
                output_key = None
            
            if output_key is not None and OS_SHIFT_PENDING:
                #if not output_key.startswith('_') and len(output_key) > 1:
                if output_key in SHIFTED:
                # if len(output_key) == 1:
                    output_key = SHIFTED[output_key]
                OS_SHIFT_PENDING = False
            
            if output_key is not None and OS_CTRL_PENDING:
                if output_key in CTRLED:
                    #output_key = CTRLED[output_key]
                    output_key = ('_ctrl', output_key)
                OS_CTRL_PENDING = False

            #if output_key in CODES:
            #    output_key = CODES[output_key]

            new_event = {'buttons': list(PENDING_BUTTONS),
                            'start_time': clock,
                            'output_key': output_key,
                            'last_output_time': 0,
                            'layer': new_layer,
                            'active': output_key is not None or new_layer is not None
                        }
            if output_key in ('_mup', '_mdwn', '_mlft', '_mrgt', '_mdul', '_mdur', '_mddl', '_mddr'):
                new_event['active'] = False

            printd('New event: {new_event}')
            EVENTS.append(new_event)
            PENDING_BUTTONS.clear()
            TICKER = 0
    
    # Check Mouse Events
    mouse_x, mouse_y = 0, 0
    if [e for e in EVENTS if e['output_key'] in ('_mlft', '_mdul', '_mddl')]:
        mouse_x -= 5
    if [e for e in EVENTS if e['output_key'] in ('_mrgt', '_mdur', '_mddr')]:
        mouse_x += 5
    if [e for e in EVENTS if e['output_key'] in ('_mup', '_mdul', '_mdur')]:
        mouse_y -= 5
    if [e for e in EVENTS if e['output_key'] in ('_mdwn', '_mddl', '_mddr')]:
        mouse_y += 5

    # Generate key press based on top active event.
    output_key = None
    if EVENTS and EVENTS[-1]['active']:
        last_event = EVENTS[-1]
        if last_event['output_key'] is not None:
            last_event['active'] = False
            output_key = last_event['output_key']
            # return(last_event['output_key'])
    triggerUinput(output_key, mouse_x, mouse_y)


def triggerUinput(keypress, mouse_x, mouse_y):
    global UINPUT
    global UINPUT_TRANSLATE

    if mouse_x or mouse_y:
        UINPUT.emit(uinput.REL_X, mouse_x, syn=False)
        UINPUT.emit(uinput.REL_Y, mouse_y)
        
    if keypress is None:
        return
    
    if isinstance(keypress, tuple):
        uinput_key = (UINPUT_TRANSLATE[keypress[0]], 
                        UINPUT_TRANSLATE[keypress[1]])
    else:
        uinput_key = UINPUT_TRANSLATE[keypress]

    print(keypress, uinput_key)
    if isinstance(uinput_key[0], (list, tuple)):
        UINPUT.emit_combo(uinput_key)
    else:
        UINPUT.emit_click(uinput_key)



if __name__ == '__main__':

    # Make sure uinput is loaded
    if not os.path.exists('/sys/modules/uinput'):
        print('Loading uinput module...')
        sp.call(['modprobe', 'uinput'])

    factory = LGPIOFactory(chip=0)
    # factory = RPiGPIOFactory()
    BUTTONS = []
    for pin in PINS:
        button = Button(pin, bounce_time=0.1, pin_factory=factory)
        button.when_pressed = event_handler
        button.when_released = event_handler
        BUTTONS.append(button)

    with uinput.Device(UINPUT_ACTIVATE) as UINPUT:
        print('Waiting for events!')
        pause()



                
