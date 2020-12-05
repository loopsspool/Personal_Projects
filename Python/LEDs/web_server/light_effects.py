import board
import neopixel
import time
import random

num_of_leds = 150
strip = neopixel.NeoPixel(board.D18, num_of_leds, auto_write = False)

colors = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]
brightness = 0

def alternating_colors (color0, color1, b):
    colors[0] = color0
    colors[1] = color1
    global brightness
    brightness = b
    apply_brightness(color0, color1)
    for i in range(0, num_of_leds - 1, 2):
        strip[i] = colors[0]
        strip[i + 1] = colors[1]
    strip.show()

# TODO: Maybe find a better way to apply brightness than globals?
    # Goal was to reduce lines to minimum at the beginning of each function
def apply_brightness(*arg):
    for i in range(len(arg)):
        g = arg[i][0] * brightness
        r = arg[i][1] * brightness
        b = arg[i][2] * brightness
        colors[i] = (g, r, b)
