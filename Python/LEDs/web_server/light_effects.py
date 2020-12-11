import board
import neopixel
import time
import random
import threading
# Note these variables will always be the same as their initial global initialization
from xmas_lights import brightness_arr

num_of_leds = 300
strip = neopixel.NeoPixel(board.D18, num_of_leds, auto_write = False)

def alternating_colors (color0, color1):
    for i in range(0, num_of_leds, 2):
        strip[i] = color0
        strip[i + 1] = color1
    strip.show()

def random_colors(other_effect):
    # This outer while loop continually keeps the thread running
    # If it were just the inner loop as soon as there is something in the other_effect queue
        # The thread would pop out of the while loop, consider it's work done and "kill" the thread
    while True:
        while other_effect.empty():
            for i in range (num_of_leds):
                strip[i] = (random.randrange(0, 255) * brightness_arr[0], random.randrange(0, 255) * brightness_arr[0], random.randrange(0, 255) * brightness_arr[0])
            strip.show()
            time.sleep(0.5)
