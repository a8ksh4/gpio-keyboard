# Gpio Keyboard
This is a chording keyboard firmware made with gpiozero and the uinput module.  Gpiozero is compatible with the raspberry pis on the most recent version of raspberry pi os at the time of tihs writing.  

It support lots of features:
* Typing
* Chords - press 'a' and 'r' to type 'f'.
* Momentary layer changes - hold a key to active a layer for a moment
* Default layer changes - set the base layer
* Oneshot Shift, Ctrl, Alt.  It does NOT currently support holding these keys and typing multiple subsequent keys.
* Mouse cursor movement.
* Mouse wheel
* Arrow keys, home, end, pgup, pgdn navigation.
  
Generally how this works is every millisecond:
* it checks the gpio pins for buttons pressed
* checks if other buttons are pressed but not yet part of an active keypress
* checks the clock to see if enough time has passed to register a chord or button press.  If not sleep, if so:
* register an active keypress (or mouse event)
* pass the event to uinput python module, which passes it to the uinput kernel module, whick tells the system the keyboard or mouse has done something. 

The keymap in this repo is for a 2-row, 5-column keyboard with a layout very close to artsey.io.  I added the 5th column to make it easier to type parens, colon, and some other stuff to make programming a little more pleasant. 

## Setup
* apt install python3-gpiozero
* apt install python3-uinput
* Update keymap.py with the pins for your keyboard.  Currently it supports only one key per pin, not matrix scanning, although this is easy to add if anyone would us it.
* Install the systemd service (need to work out more details here)
** sudo ln -s /home/myuser/git/Pocket/keeb.service /etc/systemd/system/
* more details here...
* if you add a key that's not listed in uinput_translate.py, it'll cause a crash, but just add it in uinput_translate.py.

## Configuration in keymap.py
There are a few important sections here:
'''PINS''' list - ordered list of gpio pin numbers corresponding with the order of keys you want to use in your LAYERS
TODO: Add support for "ROWS", "COLS", and DIODE_DIRECTION=ROWS2COLS/COLS2ROWS for matrix scanning.

'''ENCODER''' list - the two encoder pins. Common is assumed to be connnected to ground, so the encoder pins will be set pull-high and active-low. Rotary encoders are treated like keys!  Put the encoder pins in your keymap and put thes same pins in the ENCODER list in the keymap file.  Then assign actions to eack "direction" like other keys.  You can have the encoder behave differently in each layer.  Only on encoder is currently supported, but it would be simple to support multiple encoders if requested. 

'''LAYERS''' list of lists - A list of key maps that are switched between using layer changes.  Special keys can be used here.  For example:
    (1, 'c') - this says if held, change layers to layer 1, and if tapped, generate the character 'c'.  Note that the 'c' can be a part of chords defined below.  So the one key can do layer chanegs when held, directly generate a keypress, or be part of a chord.

'''CHORDS''' dictionary with dictionary-keys being lists of keys from the above layers that, when observed together as a chord, will generate a different result, the dictionary value.  For example:
     ('y', 'e'):    'c',
Says that if I press the y and e keys together, generate a 'c' keypress.  And:
    ('e', 'r', 'i'):            ('_set_base', 4),   
    ('_left', '_up', '_rght'):  ('_set_base', 0),
These use the same three physical key switchec on the keyboard to change the default layer between between the normal base layer and a navigation layer. 

### Special keys, syntax, etc.
Here's a list of supported things you can put in your keymap.  uinput has it's own naming for keys, but it's terse and I wanted something more concise and readable for keymaps, so I translate what you see here to uinput stuff.
* Lower case letters: 'a', 'b', ...
* Upper case letters: 'A', 'B', ...
* Numbers: '1', '2', ...   Note that these need to be quoted like the letters.  An unquoted number indicates a layer change when the key is held!
* Number row symbols: '!', '@', '#', ...  That you would normally type by holding shift and typing a number key.
* Symbols: ';', '.', ']'...
* Shifted Symbols: ':', '>', '}'...
* Functional stuff: '_esc', '_tab', '_entr', '  ' (space)
* Navigation: '_left', '_rght', '_up', '_down', '_pgup', '_pgdn', '_home',  '_end'
* Mouse Nav: '_mlft', '_mrgt', '_mup', '_mdwn', '_mbt1', '_mbt2', '_mbt3'
* Mouse Diagonals: '_mdur' (up right), '_mdul', '_mddr" (down right), '_mddl'
* Mouse Scroll Wheel: '_scup', '_scdn'
* One-Shot Operations: '_os_shift', '_os_ctrl', '_os_alt'
* Layer Changing: '(_set_base, 2)' to change the base layer, or just an unquoted number to momentarily change layer as long as the key is held.

Currently NOT supported:
* '_shift', '_ctrl', '_alt' standard keys.  Currently only one-shot is supported.  I'll need to refactor the code a bit to support these keys.

Keymap vs uinput_translate.py
Every key/behavior in the keymap must have a corresponding entry in the uinput_translate file that says what will be passed to uinput for the behavior.  Normally this is a simple mapping like this...
* Keymap has the letter 'a'.
* Uinput_translate has:     'a': uinput.KEY_A,

But we can do more interesting stuff like this:
* Keymap has: '_alta', meaning alt + tab
* Uinput_translate has: '_alta': (uinput.KEY_LEFTALT, uinput.KEY_TAB),

When an entry has a list of actions like this, we'll emit the first key, then the second (and third ...), and unpress them in the same order.  

