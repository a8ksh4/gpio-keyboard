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

