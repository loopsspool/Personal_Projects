import board
import neopixel
import time
import random
import threading

num_of_leds = 300
strip = neopixel.NeoPixel(board.D18, num_of_leds, auto_write = False)

def single_color(color):
    strip.fill(color)
    strip.show()

def off():
    strip.fill((0, 0, 0))
    strip.show()

def alternating_colors(color_arr):
    for i in range(0, num_of_leds, 2):
        strip[i] = color_arr[0]
        strip[i + 1] = color_arr[1]
    strip.show()

def random_colors(looping_event, brightness_arr):
    while looping_event.is_set():
        print(brightness_arr[0])
        for i in range (num_of_leds):
            strip[i] = (random.randrange(0, 255) * brightness_arr[0], random.randrange(0, 255) * brightness_arr[0], random.randrange(0, 255) * brightness_arr[0])
        strip.show()
        time.sleep(0.5)
