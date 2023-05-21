from machine import ADC, Pin
import time

BATTERY_PIN = 28
BATTERY_INTERVAL_SECONDS = 15

KEEB_PINS = [15, 14, 13, 12, 16, 17, 18, 19]
POLL_INTERVAL_SECONDS = 0.01


adc = ADC(Pin(28))
pins = [Pin(n, Pin.IN) for n in KEEB_PINS]

last_buttons = None
last_time = None

while True:
    battery_volts = adc.read_u16() * 2 * 3.3 / 65535
    print(f'battery {battery_volts}')
    buttons = [p.value() for p in pins]

    if last_buttons is None or last != buttons:
        last_buttons = buttons
        print(f'buttons {' '.join(buttons))
    print

