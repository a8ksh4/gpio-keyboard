import gc
from machine import ADC, Pin
import time


PI_SHIM_PIN = 19
SYS_PW_PIN = 18

BATTERY_PIN = 28
BATTERY_INTERVAL_SECONDS = 15

ROWS = (2, 3, 4, 5, 17, 16)
COLS = (6, 7, 8, 9, 10, 11, 12, 13, 14, 15)

SYSTEM_SHUTDOWN_KEYS = set((48, 41, 58, 51))
MICROPYTHON_EXIT_KEYS = set((0, 19, 20, 9, 10, 29))
VOLTAGE_WARNING_LEVEL = 3.2
SYSTEM_SHUTDOWN_LEVEL = 3.1
HARD_POWER_LEVEL = 3.0

INACTIVE_SLEEP_TIMER = 5 # auto shut down afther this many minutes?

# Features List
# auto shudown at low battery
# auto shutdown on no activity
# wake up/boot the pi on activity if prev auto shutdown (not total system off)
# dim the screen when idle
# pass through screen brighness?  No, do that in sw on the pi.


POLL_INTERVAL_SECONDS = 0.005

adc = ADC(Pin(29))
# Turn on the pi first-thing, value=1
pi_shim = Pin(PI_SHIM_PIN, Pin.OUT, value=1)
# Don't shut down system poweer, value=0
sys_pw = Pin(SYS_PW_PIN, Pin.OUT, value=0)

time.sleep(2)

cols = [Pin(n, Pin.OUT, value=0) for n in COLS]
rows = [Pin(n, Pin.IN, Pin.PULL_DOWN) for n in ROWS]
all_buttons = [(c, r) for r in rows for c in cols]
values = [0 for b in all_buttons]


def getBatteryVoltage():
    #return adc.read_u16() * 2 * 3.3 / 65535
    return adc.read_u16() * 3 * 3.3 * 4.2 / (65535 * 4.0)


def getPressedButtons():
    out = set()
    for n, (c, r) in enumerate(all_buttons):
        c.on()
        if r.value():
            out.add(n)
        c.off()
    return out


last_buttons = None
last_buttons_time = 0
last_battery_time = 0
last_battery_warn = 0

toggle = False

while True:
    time_s = time.ticks_ms() / 1000
            
    if last_battery_time is None:
        last_battery_time = 0
    s_since_battery = time_s - last_battery_time
    
    if s_since_battery > BATTERY_INTERVAL_SECONDS:
        last_battery_time = time_s
        battery_volts = getBatteryVoltage()
        print(f'battery {battery_volts}')
        if not last_buttons:
            gc.collect()
    
    if battery_volts < HARD_POWER_LEVEL and pi_shim.value():
        #sys_pw.value(1)
        pass
        
    if battery_volts < SYSTEM_SHUTDOWN_LEVEL:
        print(f'shutdown Battery below {SYSTEM_SHUTDOWN_LEVEL}!')
        time.sleep(10)
        sys_pw.value(1)
    
    if (battery_volts < VOLTAGE_WARNING_LEVEL
            and (time_s - last_battery_warn) > 60):
        last_battery_warn = time_s
        print(f'low_battery')

    buttons = getPressedButtons()
    if set(buttons) == SYSTEM_SHUTDOWN_KEYS:
        print('shutdown Shutdown keys pressed.')
        time.sleep(10)
        sys_pw.value(1)
    if set(buttons) == MICROPYTHON_EXIT_KEYS:
        print('dropping to python prompt')
        exit()

    elif last_buttons is None or last_buttons != buttons:
        last_buttons = buttons
        time_delta_s = time_s - last_buttons_time
        last_buttons_time = time_s
        buttons = ' '.join(str(b) for b in buttons)
        print(f'buttons {buttons}')
        toggle = True
    
    elif toggle:
        buttons = ' '.join(str(b) for b in buttons)
        print(f'buttons {buttons}')
        toggle = False

    time.sleep(POLL_INTERVAL_SECONDS)
    
