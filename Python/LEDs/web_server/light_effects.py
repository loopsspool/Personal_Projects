import board
import neopixel
import time
import random
import math

num_of_leds = 350
strip = neopixel.NeoPixel(board.D18, num_of_leds, auto_write = False)
# This controls the time sleep of animated functions
    # Must be a global to accurately store timing data across changes
amount = 0.5

def set_amount(animated_effect_speed_queue):
    global amount
    # 1 - to make slider go from slow to fast
    amount = 1 - float(animated_effect_speed_queue.get())/100


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

def random_colors(brightness_arr, animated_effect_speed_queue, looping_effect_queue, static_effect_queue):
    
    while looping_effect_queue.empty() and static_effect_queue.empty():
        for i in range (num_of_leds):
            strip[i] = (random.randrange(0, 255) * brightness_arr[0], random.randrange(0, 255) * brightness_arr[0], random.randrange(0, 255) * brightness_arr[0])
        strip.show()

        if not animated_effect_speed_queue.empty():
            set_amount(animated_effect_speed_queue)

        global amount
        time.sleep(amount)

def animated_alternating_colors(color_arr, animated_effect_speed_queue, looping_effect_queue, static_effect_queue):
    
    color0 = color_arr[0]
    color1 = color_arr[1]
    while looping_effect_queue.empty() and static_effect_queue.empty():
        for i in range(0, num_of_leds, 2):
            strip[i] = color0
            strip[i + 1] = color1

        strip.show()
        color0, color1 = color1, color0

        if not animated_effect_speed_queue.empty():
            set_amount(animated_effect_speed_queue)

        global amount
        print(amount)
        if (amount < 0.07):
            time.sleep(0.07)
        else:
            time.sleep(amount)


def twinkle(color_arr, animated_effect_speed_queue, looping_effect_queue, static_effect_queue):
    brightness = [0] * num_of_leds
    brightness_direction = [0] * num_of_leds
    # Adjusting slider to an appropriate range for twinkle
    global amount
    amount = (1 - amount)/10
    ceil_brightness = 0.8
    
    for i in range(num_of_leds):
        brightness[i] = random.uniform(.1, ceil_brightness)
        brightness_direction[i] = random.random() < 0.5
    
    while looping_effect_queue.empty() and static_effect_queue.empty():
        if not animated_effect_speed_queue.empty():
            amount = float(animated_effect_speed_queue.get())/1000

        for i in range(num_of_leds):
            # Checking bounds
            if (brightness[i] + amount) >= ceil_brightness:
                brightness_direction[i] = False
            if (brightness[i] - amount) <= amount:
                brightness_direction[i] = True
            
            # Incrementing pixel brightness
            if brightness_direction[i] == True:
                brightness[i] += amount
            else:
                brightness[i] -= amount

            # Applying brightness
            g = math.ceil(color_arr[0][0] * brightness[i])
            r = math.ceil(color_arr[0][1] * brightness[i])
            b = math.ceil(color_arr[0][2] * brightness[i])
            strip[i] = (g, r, b)

        strip.show()
    
    # Readjusting amount to an appropriate range for other animated functions
    # Happens when the while loop is broken out of
    amount = (1 - (amount * 10))