# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import neopixel

# set pixel data pin
pixel_pin = board.D21

# The number of NeoPixels
num_pixels = 1

# set colours
dsky_green =	(94,255,0)
black =			(0,0,0)

# The order of the pixel colors 
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

pixels.fill(black) # black / off
pixels.show()

while True:

    pixels.fill(dsky_green) # green / on
    pixels.show()
    



