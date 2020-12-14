import board
import neopixel
import time
import random
import math

num_of_leds = 350
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

def twinkle(color_arr, looping_effect_queue, static_effect_queue):
    brightness = [0] * num_of_leds
    brightness_direction = [0] * num_of_leds
    brightness_inc = 0.03
    ceil_brightness = 0.7
    
    for i in range(num_of_leds):
        brightness[i] = random.uniform(3 * brightness_inc, ceil_brightness)
        brightness_direction[i] = random.random() < 0.5
    
    while looping_effect_queue.empty() and static_effect_queue.empty():
        for i in range(num_of_leds):
            # Checking bounds
            if (brightness[i] + brightness_inc) >= ceil_brightness:
                brightness_direction[i] = False
            if (brightness[i] - brightness_inc) <= brightness_inc:
                brightness_direction[i] = True
            
            # Incrementing pixel brightness
            if brightness_direction[i] == True:
                brightness[i] += brightness_inc
            else:
                brightness[i] -= brightness_inc

            #print("Going up?:", brightness_direction[i])
            #print(brightness[i])

            # Applying brightness
            g = math.ceil(color_arr[0][0] * brightness[i])
            r = math.ceil(color_arr[0][1] * brightness[i])
            b = math.ceil(color_arr[0][2] * brightness[i])
            strip[i] = (g, r, b)

        strip.show()
        #time.sleep(0.1)