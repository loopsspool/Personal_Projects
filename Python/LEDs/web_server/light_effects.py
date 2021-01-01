import board
import neopixel
import time
import random
import math

num_of_leds = 350
strip = neopixel.NeoPixel(board.D18, num_of_leds, auto_write = False, pixel_order = 'GRB')
amount_of_colors = 1
block_size = 1
# This controls the time sleep of animated functions
    # Must be a global to accurately store timing data across changes
sleep_amount = 0.5

def set_sleep_amount(queue_dict):
    global sleep_amount
    # 1 - to make slider go from slow to fast
    sleep_amount = 1 - float(queue_dict["animated effect speed queue"].get())/100


############################## STATIC FUNCTIONS ##############################

def off():
    strip.fill((0, 0, 0))
    strip.show()


def color(color_arr, amount_of_colors, block_size):
    
    color_acc = 0
    for i in range(0, num_of_leds, block_size):
        # Putting in each color
        for ii in range(block_size):
            # But only if it's on the strip
            if (i + ii) < num_of_leds:
                strip[i + ii] = color_arr[color_acc]
        # Updating the color
        color_acc += 1
        color_acc %= amount_of_colors

    strip.show()


############################## ANIMATED FUNCTIONS ##############################

def random_colors(brightness_arr, queue_dict):
    
    global sleep_amount
    while queue_dict["looping effect queue"].empty() and queue_dict["static effect queue"].empty():
        for i in range (num_of_leds):
            strip[i] = (random.randrange(0, 255) * brightness_arr[0], random.randrange(0, 255) * brightness_arr[0], random.randrange(0, 255) * brightness_arr[0])
        strip.show()

        # Checking if animated speed slider has changed
        if not queue_dict["animated effect speed queue"].empty():
            set_sleep_amount(queue_dict)

        # Prevents stroke-inducing light changes
        if (sleep_amount < 0.07):
            time.sleep(0.07)
        else:
            time.sleep(sleep_amount)


def animated_alternating_colors(color_arr, queue_dict):
    
    global amount_of_colors
    global sleep_amount
    global block_size
    color_acc = 0 # Color accumulator to animate the effect
    starter_acc = 0
    while queue_dict["looping effect queue"].empty() and queue_dict["static effect queue"].empty():

        # Checking for colors added/removed
        if not queue_dict["amount of colors queue"].empty():
            amount_of_colors = int(queue_dict["amount of colors queue"].get())

        # Checking for the style of multiple colors
        if not queue_dict["block size queue"].empty():
            block_size= int(queue_dict["block size queue"].get())

        for i in range(0, num_of_leds, block_size):
            # Putting in each color
            for ii in range(block_size):
                # But only if it's on the strip
                if (i + ii) < num_of_leds:
                    strip[i + ii] = color_arr[color_acc]
            # Updating the color
            color_acc += 1
            color_acc %= amount_of_colors

        strip.show()

        if not queue_dict["animated effect speed queue"].empty():
            set_sleep_amount(queue_dict)

        # Prevents the change of colors occuring so fast the strip appears one color
        if (sleep_amount < 0.07):
            time.sleep(0.07)
        else:
            time.sleep(sleep_amount)

        # Incrementing the accumulator to cause the animation effect
        color_acc = 0
        starter_acc += 1
        starter_acc %= amount_of_colors
        color_acc += starter_acc


def twinkle(color_arr, queue_dict):
    brightness = [0] * num_of_leds
    brightness_direction = [0] * num_of_leds
    # Adjusting slider to an appropriate range for twinkle
    global sleep_amount
    sleep_amount = (1 - sleep_amount)/10
    ceil_brightness = 0.8
    
    # Initializing brightnesses and brightness direction
    for i in range(num_of_leds):
        brightness[i] = random.uniform(.1, ceil_brightness)
        brightness_direction[i] = random.random() < 0.5
    
    global amount_of_colors
    global block_size
    while queue_dict["looping effect queue"].empty() and queue_dict["static effect queue"].empty():
        # Checking if animated speed slider has changed
        if not queue_dict["animated effect speed queue"].empty():
            sleep_amount = float(queue_dict["animated effect speed queue"].get())/1000

        # So twinkle isn't so incredibly slow and "pixelated"
        if (sleep_amount < 0.008):
            sleep_amount = 0.008

        # Checking if amount of colors has changed
        if not queue_dict["amount of colors queue"].empty():
            amount_of_colors = int(queue_dict["amount of colors queue"].get())

        # Checking for the style of multiple colors
        if not queue_dict["block size queue"].empty():
            block_size= int(queue_dict["block size queue"].get())

        color_acc = 0
        for i in range(0, num_of_leds, block_size):
            for ii in range(block_size):
                # If the pixel is on the strip
                if (i + ii) < num_of_leds:
                        
                    # Checking bounds
                    if (brightness[i + ii] + sleep_amount) >= ceil_brightness:
                        brightness_direction[i + ii] = False
                    if (brightness[i + ii] - sleep_amount) <= sleep_amount:
                        brightness_direction[i + ii] = True
                    
                    # Incrementing pixel brightness
                    if brightness_direction[i + ii] == True:
                        brightness[i + ii] += sleep_amount
                    else:
                        brightness[i + ii] -= sleep_amount

                    # Applying brightness and color
                    g = math.ceil(color_arr[color_acc][0] * brightness[i + ii])
                    r = math.ceil(color_arr[color_acc][1] * brightness[i + ii])
                    b = math.ceil(color_arr[color_acc][2] * brightness[i + ii])
                    strip[i + ii] = (g, r, b)
            # Updating the color
            color_acc += 1
            color_acc %= amount_of_colors

        strip.show()
    
    # Readjusting sleep_amount to an appropriate range for other animated functions
    # Happens when the while loop is broken out of
    sleep_amount = (1 - (sleep_amount * 10))