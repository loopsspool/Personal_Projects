import board
import neopixel
import time
import random

num_of_leds = 300
strip = neopixel.NeoPixel(board.D18, num_of_leds, auto_write = False)

def alternating_colors (color0, color1):
    for i in range(0, num_of_leds, 2):
        strip[i] = color0
        strip[i + 1] = color1
    strip.show()

