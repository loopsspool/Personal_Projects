import board
import neopixel
import time
import random

num_of_leds = 300
strip = neopixel.NeoPixel(board.D18, num_of_leds, auto_write = False)

############################## STATIC FUNCTIONS ##############################

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



############################## ANIMATED FUNCTIONS ##############################

def random_colors(brightness_arr, looping_effect_queue, static_effect_queue):
    while looping_effect_queue.empty() and static_effect_queue.empty():
        for i in range (num_of_leds):
            strip[i] = (random.randrange(0, 255) * brightness_arr[0], random.randrange(0, 255) * brightness_arr[0], random.randrange(0, 255) * brightness_arr[0])
        strip.show()
        time.sleep(0.5)

def animated_alternating_colors(color_arr, looping_effect_queue, static_effect_queue):
    color0 = color_arr[0]
    color1 = color_arr[1]
    while looping_effect_queue.empty() and static_effect_queue.empty():
        for i in range(0, num_of_leds, 2):
            strip[i] = color0
            strip[i + 1] = color1
        strip.show()
        color0, color1 = color1, color0
        time.sleep(0.5)
