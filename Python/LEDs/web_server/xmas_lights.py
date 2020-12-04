import board
import neopixel
import time
import random
from light_effects import *
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# number of LEDs
# TODO: These should be omitted and transfered exclusively to light_effects.py
num_of_leds = 150
strip = neopixel.NeoPixel(board.D18, num_of_leds, auto_write = False)

#define LED GPIO pin
leds = 18

# Define led pin as output
GPIO.setup(leds, GPIO.OUT)   

# Two color effects array
two_color_effects = ["Alternating colors"]

# Three color effects

@app.route("/")
def index():
	templateData = {
              'title' : 'Xmas lights!',
              #'led_status' : led_status
    }
	return render_template('index.html', **templateData)
	
# Just a note....
# elements on the page have to be used before you can request their form data
# For example a color must be chosen with no call to its value on this file
# Before it is populated into the request multiDict
# Only then can you access it here without a bad key request error
@app.route("/", methods = ["GET", "POST"])
def action():
    # Reads action and acts
	effect = request.form["effects"]
	# TODO: Change brightness for each color?
	brightness = float(request.form["brightness"])/100
	color0 = hex_to_grb(request.form["color0"])
	# This is to debug what keys are actually posted currently to the form
	#print(request.form)

	if effect in two_color_effects:
		color1 = hex_to_grb(request.form["color1"])

	if effect == "on":
		strip.fill((color0[0] * brightness, color0[1] * brightness, color0[2] * brightness))
		strip.show()

	if effect == "off":
		strip.fill((0, 0, 0))
		strip.show()
	
	if effect == "random":
		# To have this infinite looping you need to enable multithreading so
			# Running the code doesn't stop the webpage from loading
		#while True:
			for i in range (num_of_leds):
				strip[i] = (random.randrange(0, 255) * brightness, random.randrange(0, 255) * brightness, random.randrange(0, 255) * brightness)
			strip.show()
			time.sleep(0.5)

	if effect == "Alternating colors":
		alternating_colors(color0, color1, brightness)

	templateData = {
              #'led_status' : led_status
	}

	return render_template('index.html', **templateData)

def hex_to_grb(hex):
	# Courtesy of: https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
	# Modified to return grb, not rgb
	hex = hex.lstrip('#')	# Removes initial hash
	rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))	# Finds rgb values
	grb = (rgb[1], rgb[0], rgb[2])	# Trades r & g values to create grb tuple
	return grb

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True) 