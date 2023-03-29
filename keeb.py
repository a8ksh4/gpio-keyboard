#!/usr/bin/env python3

#import collections
from keymap import LAYERS, CHORDS, PINS, ENCODER
from keys import SHIFTED, CTRLED, MOUSE_CODES #, CODES
import lgpio as sbc
import os
import subprocess as sp
#import threading as th
import time
import uinput
from uinput_translate import UINPUT_ACTIVATE, UINPUT_TRANSLATE

CHIP = 0 # sholdn't need to change on raspberry pi

FREQUENCY = 100 # Times per second to poll for changes
SLEEP_TIME = 1 / FREQUENCY

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
OS_ALT_PENDING = False
TIMER = None
DEBUG = False
DELAYED_INPUT = [] # interface for other tools to ask for something to be typed.


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


def poll_keys(buttons_pressed, device):
    #print('FOO', foo)
    global TICKER  
    global HOLDTIME
    global BASE_LAYER
    global EVENTS
    global PENDING_BUTTONS
    global PINS
    global OS_SHIFT_PENDING
    global OS_CTRL_PENDING
    global OS_ALT_PENDING
    global DELAYED_INPUT
    global MOUSE_CODES

    # clock = time.ticks_ms()
    clock = time_ms()

    current_layer = [BASE_LAYER,] + [e['layer'] for e in EVENTS if e['layer']]
    current_layer = current_layer[-1]

    # Remove events whos buttons are no longer pressed.
    for event in EVENTS:
        still_pressed = [b for b in event['buttons'] if b in buttons_pressed]
        if not still_pressed:
            event['status'] = 'released'

    # Remove buttons from buttons_pressed if associated with an event
    all_event_butons = sum([e['buttons'] for e in EVENTS], [])
    #print('all event buttons:', all_event_butons)
    buttons_pressed = [b for b in buttons_pressed if b not in all_event_butons]

    # Move buttons_pressed to pending - pending buttons is buttons 
    # that have been pressed but are not associated with an event.
    PENDING_BUTTONS.update(buttons_pressed)

    if PENDING_BUTTONS:
        if not TICKER:
            TICKER = clock
        #print('Pending:', PENDING_BUTTONS)

        # TODO: maybe separate hold times for layer stuff vs chords. 
        
        # DO WE MEET THE CONDITIONS TO START A NEW EVENT?
        if ( len(PENDING_BUTTONS) > len(buttons_pressed)  # one or more keys released
                or clock - TICKER > HOLDTIME ):           # hold time exceeded
            
            tap =  clock - TICKER < HOLDTIME

            printd(f'{(len(PENDING_BUTTONS), len(buttons_pressed), clock, TICKER, clock-TICKER)}')
            #print(PENDING_BUTTONS, current_layer, tap)
            output_key, new_layer = get_output_key(PENDING_BUTTONS, current_layer, tap)
            print(f'output_key: {output_key}, new_layer: {new_layer}')

            #print(output_key, new_layer)
            if output_key == '_set_base':
                BASE_LAYER = new_layer
                output_key, new_layer = None, None

            if output_key == '_os_shft':
                OS_SHIFT_PENDING = True
                output_key = None

            if output_key == '_os_ctrl':
                OS_CTRL_PENDING = True
                output_key = None
                
            if output_key == '_os_alt':
                OS_ALT_PENDING = True
                output_key = None
            
            if output_key is not None and OS_SHIFT_PENDING:
                if output_key in SHIFTED:
                    output_key = SHIFTED[output_key]
                OS_SHIFT_PENDING = False
            
            if output_key is not None and OS_CTRL_PENDING:
                output_key = ('_ctrl', output_key)
                OS_CTRL_PENDING = False
                
            if output_key is not None and OS_ALT_PENDING:
                output_key = ('_alt', output_key)
                OS_ALT_PENDING = False
            
            # align on tuple output_key
            if not isinstance(output_key, tuple):
                output_key = (output_key,)
                
            
            new_event = {'buttons': list(PENDING_BUTTONS),
                            'output_keys': output_key,
                            'layer': new_layer,
                            'status': 'new',
                            'uinput_codes': []
                        }
            
            for ok in output_key:
                if ok in MOUSE_CODES:
                    new_event['status'] = 'mouse'
                    break

            print(f'New event: {new_event}')
            EVENTS.append(new_event)
            PENDING_BUTTONS.clear()
            TICKER = 0
    
    # Check Mouse Events
    mouse_x, mouse_y, mouse_wheel= 0, 0, 0
    if [e for e in EVENTS if e['output_keys'] in ('_mlft', '_mdul', '_mddl')]:
        mouse_x -= 5
    if [e for e in EVENTS if e['output_keys'] in ('_mrgt', '_mdur', '_mddr')]:
        mouse_x += 5
    if [e for e in EVENTS if e['output_keys'] in ('_mup', '_mdul', '_mdur')]:
        mouse_y -= 5
    if [e for e in EVENTS if e['output_keys'] in ('_mdwn', '_mddl', '_mddr')]:
        mouse_y += 5

    # Check Mouse Wheel Events:
    mouse_wheel = 0
    for event in EVENTS:
        if event['status'] != 'mouse':
            continue
        
        event['status'] = 'mouse_done'
        #if event['output_keys'] == '_mwup':
        if '_mwup' in event['output_keys']:
            print('mouse wheel up')
            mouse_wheel = 1
        #elif event['output_keys'] == '_mwdn':
        elif '_mwdn' in event['output_keys']:
            print('mouse wheel down')
            mouse_wheel = -1

    # Unpress ended events
    for event in EVENTS:
        if event['status'] != 'released':
            continue

        for uinput_code in event['uinput_codes'][::-1]:
            print('unpressing', uinput_code)
            device.emit(uinput_code, 0, syn=True)
            time.sleep(0.01)
        event['status'] = 'delete'
        print(event)
    
    # Delete done events
    EVENTS = [e for e in EVENTS if e['status'] != 'delete']

    # Check for ctrl alt shift state
    alt_pressed = [e for e in EVENTS if '_alt' in e['output_keys'] and e['status'] == 'active']
    shift_pressed = [e for e in EVENTS if '_shift' in e['output_keys'] and e['status'] == 'active']
    ctrl_pressed = [e for e in EVENTS if '_ctrl' in e['output_keys'] and e['status'] == 'active']
        
    # Generate key press based on top active event.
    if EVENTS and EVENTS[-1]['status'] == 'new':
        last_event = EVENTS[-1]
        last_event['status'] = 'active'
        effective_keys = [k for k in last_event['output_keys'] if
                            not (k == '_alt' and alt_pressed) and
                            not (k == '_shift' and shift_pressed) and
                            not (k == '_ctrl' and ctrl_pressed)]

        uinput_codes = [UINPUT_TRANSLATE[k] for k in effective_keys 
                            if k is not None
                            and k not in MOUSE_CODES]
        # uinput_codes = [c if isinstance(c[0], tuple) else (c,) for c in uinput_codes]
        # uinput_codes = [c for l in uinput_codes for c in l]

        unpress_later = []
        for uinput_code in uinput_codes:
            if isinstance(uinput_code[0], tuple):
                temp_codes = uinput_code[:-1]
                keep = uinput_code[-1]
            else: 
                temp_codes = []
                keep = uinput_code
            unpress_later.append(keep)
                
            for temp_code in temp_codes:
                print('temp press', temp_code)
                device.emit(temp_code, 1, syn=True)
                time.sleep(0.01)

            print('pressing', keep)
            device.emit(keep, 1, syn=True)
            time.sleep(0.01)
            for temp_code in temp_codes:
                print('temp unpress', temp_code)
                device.emit(temp_code, 0, syn=True)
                time.sleep(0.01)
        last_event['uinput_codes'] = unpress_later

            
    # Generate mouse movement
    if mouse_x or mouse_y:
        device.emit(uinput.REL_X, mouse_x, syn=False)
        device.emit(uinput.REL_Y, mouse_y, syn=True)
    if mouse_wheel != 0:
        print('mouse wheel', mouse_wheel)
        device.emit(uinput.REL_WHEEL, mouse_wheel, syn=True)

    # if keypress is None:
    #     continue
    # if isinstance(keypress, tuple):
    #     uinput_key = [UINPUT_TRANSLATE[keypress[0]], 
    #                     UINPUT_TRANSLATE[keypress[1]]]
    # else:
    #     uinput_key = UINPUT_TRANSLATE[keypress]

    # print(keypress, uinput_key)
    # if isinstance(uinput_key[0], (list, tuple)):
    #     emit_these = uinput_key[:-1]
    #     click_this = uinput_key[-1]
    #     # first = uinput_key[0]
    #     # second = uinput_key[1]

    #     for et in emit_these:
    #         device.emit(et, 1, syn=True)
    #         time.sleep(0.05)
            
    #     # device.emit(first, 1, syn=True)
    #     # time.sleep(0.05)
    #     device.emit_click(click_this, syn=True)
    #     # time.sleep(0.05)
    #     # device.emit(first, 0, syn=True)
    #     for et in emit_these:
    #         device.emit(et, 0, syn=True)
    #         time.sleep(0.05)

    # else:
    #     device.emit_click(uinput_key)

    # emit a python ctrl c combo with python uinput
    #device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_C])




if __name__ == '__main__':

    # Make sure uinput is loaded
    if not os.path.exists('/sys/modules/uinput'):
        print('Loading uinput module...')
        sp.call(['modprobe', 'uinput'])

    handle = sbc.gpiochip_open(CHIP)
    sbc.group_claim_input(handle, PINS, sbc.SET_BIAS_PULL_UP | sbc.SET_ACTIVE_LOW)
    

    print(UINPUT_ACTIVATE)
    with uinput.Device(UINPUT_ACTIVATE) as device:
        #foo, mask = sbc.group_read(handle, PINS[0])
        mask = None
        while True:
            time.sleep(SLEEP_TIME)

            foo, new_mask = sbc.group_read(handle, PINS[0])
            if new_mask == mask and not EVENTS:
                continue
            #same = mask ^ new_mask
            active = [n for n in range(32) if new_mask & 2**n]
            # keypress, mouse_x, mouse_y = poll_keys(active)
            poll_keys(active, device)

                


                
