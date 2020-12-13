import board
import neopixel
import time
import random
from light_effects import *
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import threading
import queue
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

# Brightness array used to store potential multiple brightnesses
# So colors can be updated accordingly
# 10 0.1's just so I don't have to adjust size each time I add a brightness slider
brightness_arr = [0.1] * 10

# Amount of colors dictionary
effect_color_amounts = {
	"Off": 1,
	"On": 1,
	"Alternating colors": 2,
	"Random": 2
}

# TODO: Test with another looping effect and running them back to back
def looping_effects_analyzer(looping_effect, looping_event, brightness_arr):
	# This wait blocks the below code until a selected looping effect triggers it to run
	looping_event.wait()

	# This while loop keeps the thread alive when it is idle
	# Otherwise when the looping event is set to false, it will exit out of its while loop in the effect function
		# Return to this thread function, see there are no more commands
			# And it will die, not to be revived
	# So in other words, don't delete this while loop lol
	while True:
		looping_effect_name = looping_effect.get()

		if looping_effect_name == "Random":
			random_colors(looping_event, brightness_arr)

looping_effects = ["Random"]
looping_effect_queue = queue.Queue()
looping_event = threading.Event()
thread = threading.Thread(target = looping_effects_analyzer, name = "looping thread", args = (looping_effect_queue, looping_event, brightness_arr,))

@app.route("/", methods = ["GET", "POST"])
def action():
	if request.method == 'POST':
		# Copies form values to be used outside this function (in getting values)
			# Form data is local to the app route, so by copying it it can be exported
		global form_data
		form_data = request.form.copy()
		# Making effect global so light_effects script can access it
			# Mainly for infinite looping functions
		global effect
		effect = get_value("effect")
		
		# This is a workaround since the checkbox unchecked won't POST data
			# aka wont show up in request dict and will throw an error
		# SO KEEP THIS AS REQUEST.FORM, NOT GET_VALUE
		try:
			# Converts string "True" to boolean True
			has_mult_brightness = (request.form["mult brightnesses"] == "True")
		except:
			has_mult_brightness = False

		brightness0 = float(get_value("brightness0"))/100
		brightness_arr[0] = brightness0

		color0 = hex_to_grb(get_value("color0"))
		# Do not need to check for multiple brightnesses since first color will always be affected by first brightness
		color0 = apply_brightness(color0)

		# This is to debug what keys are actually posted currently to the form
		#print(request.form)

		# If effect has multiple colors/brightnesses they are grabbed here
		if effect_color_amounts[effect] == 2:
			color1 = hex_to_grb(get_value("color1"))
			if (has_mult_brightness):
				brightness1 = float(get_value("brightness1"))/100
				brightness_arr[1] = brightness1
				color1 = apply_brightness(color1, 1)
			else:
				color1 = apply_brightness(color1)

		if effect in looping_effects:
			looping_effect_queue.put_nowait(effect)
			looping_event.set()
		else:
			looping_event.clear()

		if effect == "On":
			strip.fill((color0[0], color0[1], color0[2]))
			strip.show()

		if effect == "Off":
			strip.fill((0, 0, 0))
			strip.show()

		if effect == "Alternating colors":
			alternating_colors(color0, color1)

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

# This is a workaround for form elements that haven't yet been initialized by a form submit causing a key error
def get_value(element_name):
	val = 0
	try:
		val = form_data[element_name]
	except Exception as e:
		val = default_form_values[element_name]

	return val

def apply_brightness(color, brightness_index = 0):
	brightness = brightness_arr[brightness_index]
	g = color[0] * brightness
	r = color[1] * brightness
	b = color[2] * brightness
	color_w_brightness = (g, r, b)
	return color_w_brightness

if __name__ == "__main__":
	thread.start()
	app.run(host='0.0.0.0', port=80, debug = True, threaded = True)