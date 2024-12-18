# Adapted from ->   CircuitPython/Raspberry Pi Pico'firmware' for The Smallest Keyboard
#                   Build video: https://www.youtube.com/watch?v=iWWTJKWFNok
#                   All files, notes, etc. are available at the project page: https://hackaday.io/project/178204-the-smallest-keyboard

# This code requires the CircuitPython installed on your Raspberry Pi Pico: https://circuitpython.org/board/raspberry_pi_pico/ (just copy the U2F file to the Pico)
# This code also requires the Adafruit HID keyboard and keycode files in your library: https://github.com/adafruit/Adafruit_CircuitPython_HID/releases/
# (download the Adafruit library that matches your CircuitPython version and copy the /lib/adafruit_hid/ files into your Pico's /lib folder)

# key matrix logical layout (rows/columns) <--> pin layout <--> Pico pin names in CircuitPython <--> physical layout/silkscreen
# var          c0   c1  c2  c3  c4  c5  c6
#    pin       1    2   4   5   6   7   9
#        name  GP0  GP1 GP2 GP3 GP4 GP5 GP6
# r0 20  GP15  null +   1   4   7   CLR null
# r1 21  GP16  VERB -   2   5   8   PRO ENTER
# r2 22  GP17  NOUN 0   3   6   9   REL RSET

import time
import board
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# optional delay before creating the HID for maximum compatibility
time.sleep(1)

# create the HID
kbd = Keyboard(usb_hid.devices)

# set up the row and column arrays
rows = []
row_pins = [board.GP15, board.GP16, board.GP17]
for row in row_pins:
    row_key = digitalio.DigitalInOut(row)
    row_key.direction = digitalio.Direction.INPUT # we're reading on the rows 
    row_key.pull = digitalio.Pull.DOWN
    rows.append(row_key)

columns = []
column_pins = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6]
for column in column_pins:
    column_key = digitalio.DigitalInOut(column)
    column_key.direction = digitalio.Direction.OUTPUT # we're writing on the columns
    columns.append(column_key)

#array of keycodes; if you want to remap see: https://circuitpython.readthedocs.io/projects/hid/en/latest/api.html#adafruit-hid-keycode-keycode /'None' values have no physical connection

keymap = [Keycode.E,	Keycode.C,	Keycode.SEVEN,	Keycode.FOUR,	Keycode.ONE,	Keycode.KEYPAD_PLUS,	Keycode.V,
          Keycode.R,	Keycode.P,	Keycode.EIGHT,	Keycode.FIVE,	Keycode.TWO,	Keycode.KEYPAD_MINUS,	Keycode.N,
          None, 	    Keycode.K,	Keycode.NINE,	Keycode.SIX,	Keycode.THREE,	Keycode.ZERO,	        None]

#main loop
while True:
    for c in columns: # for each column
        c.value=1 # set column c to high
        for r in rows: # and then for each row
            if r.value: # if a keypress is detected (high column output --> switch closing circuit --> high row input)
                while r.value: # wait until the key is released, which avoids sending duplicate keypresses
                    time.sleep(0.01) # sleep briefly before checking back
                key = rows.index(r) * 7 + columns.index(c) # identify the key pressed via the index of the current row (r) and column (c)
                print(rows.index(r))
                print(columns.index(c))
                kbd.press((keymap[key])) # press the key
                kbd.release_all() # then release all keys pressed
        c.value=0 # return the column to a low state, in preparation for the next column in the loop
