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
num_of_leds = 300
strip = neopixel.NeoPixel(board.D18, num_of_leds, auto_write = False)

#define LED GPIO pin
leds = 18

# Define led pin as output
GPIO.setup(leds, GPIO.OUT)   

# Workaround for form elements not yet being initialized into form.request
# Won't work with HTML onload because all code files are validated first
# So still an error in python refrencing a bad key in form.request
# So default form values are used in a try except block until a form value is changed
# At which point the whole form submits and the elements will be loaded into form.request
default_form_values = {
	"effect": "On",
	"color0": "#FF4614",
	"color1": "#FF4614",
	"mult brightnesses": False,
	"brightness0": 50,
	"brightness1": 50,
	"brightness2": 50
	}

# Amount of colors dictionary
effect_color_amounts = {
	"Off": 1,
	"On": 1,
	"Alternating colors": 2,
	"Random": 2
}

@app.route("/", methods = ["GET", "POST"])
def action():
	if request.method == 'POST':
		# Grabbing all necessary initial form elements
		effect = get_value("effect")
		
		# This is a workaround since the checkbox unchecked won't POST data
			# aka wont show up in request dict and will throw an error
		try:
			# Converts string "True" to boolean True
			has_mult_brightness = (request.form["mult brightnesses"] == "True")
		except:
			has_mult_brightness = False

		brightness0 = float(get_value("brightness0"))/100
		color0 = hex_to_grb(get_value("color0"))
		brightness2 = float(get_value("brightness2"))/100

		# This is to debug what keys are actually posted currently to the form
		#print(request.form)

		# If effect has multiple colors/brightnesses they are grabbed here
		if effect_color_amounts[effect] == 2:
			color1 = hex_to_grb(get_value("color1"))
			if (has_mult_brightness):
				brightness1 = float(get_value("brightness1"))/100

		# Actually applying the brightnesses



		if effect == "On":
			strip.fill((color0[0] * brightness0, color0[1] * brightness0, color0[2] * brightness0))
			strip.show()

		if effect == "Off":
			strip.fill((0, 0, 0))
			strip.show()
		
		if effect == "Random":
			# To have this infinite looping you need to enable multithreading so
				# Running the code doesn't stop the webpage from loading
			while True:
				for i in range (num_of_leds):
					strip[i] = (random.randrange(0, 255) * brightness, random.randrange(0, 255) * brightness, random.randrange(0, 255) * brightness)
				strip.show()
				time.sleep(0.5)

		if effect == "Alternating colors":
			alternating_colors(color0, color1, brightness0)

		return render_template('index.html')
	
	else:
		return render_template('index.html')

def hex_to_grb(hex):
	# Courtesy of: https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
	# Modified to return grb, not rgb
	hex = hex.lstrip('#')	# Removes initial hash
	rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))	# Finds rgb values
	grb = (rgb[1], rgb[0], rgb[2])	# Trades r & g values to create grb tuple
	return grb

# This is a workaround for form elements that haven't yet been initialized by a form submit
def get_value(element_name):
	val = 0
	try:
		val = form.request[element_name]
	except:
		val = default_form_values[element_name]

	return val

# def apply_brightness():
# 	print("nty")

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, threaded = True) 