from machine import ADC, Pin
import time

BATTERY_PIN = 28
BATTERY_INTERVAL_SECONDS = 15

# KEEB_PINS = [15, 14, 13, 12, 16, 17, 18, 19]
KEEB_PINS = (12, 13, 14, 15, 
             19, 18, 17, 16)
POLL_INTERVAL_SECONDS = 0.01


adc = ADC(Pin(28))
pins = [Pin(n, Pin.IN, Pin.PULL_UP) for n in KEEB_PINS]

last_buttons = None
last_buttons_time = 0
last_battery_time = 0

toggle = False

while True:
    time_s = time.ticks_ms() / 1000

    if last_battery_time is None:
        last_battery_time = 0
    s_since_battery = time_s - last_battery_time
    if s_since_battery > BATTERY_INTERVAL_SECONDS:
        last_battery_time = time_s
        battery_volts = adc.read_u16() * 2 * 3.3 / 65535
        print(f'battery {battery_volts}')

    buttons = ' '.join([str(p.value()) for p in pins])
    if last_buttons is None or last_buttons != buttons:
        last_buttons = buttons
        time_delta_s = time_s - last_buttons_time
        last_buttons_time = time_s
        #print(f'buttons {time_delta_s} {buttons}')
        print('buttons', time_delta_s, buttons)
        toggle = True
    
    elif toggle:
        print('buttons', time_delta_s, buttons)
        toggle = False

    time.sleep(POLL_INTERVAL_SECONDS)

