import board
import neopixel
import time
import random
from light_effects import *
from flask import Flask, render_template, request
import threading
import queue

app = Flask(__name__, template_folder = '', static_folder = '', static_url_path = '')

# Workaround for form elements not yet being initialized into form.request
# Won't work with HTML onload because all code files are validated first
# So there was still an error in python refrencing a bad key in form.request
# So default form values are used in a try except block until a form value is changed
# At which point the whole form submits and the elements will be loaded into form.request
default_form_values = {
	"effect": "Single color",
	"color0": "#FF4614",
	"color1": "#FF4614",
	"mult brightnesses checkbox": False,
	"brightness0": 50,
	"brightness1": 50,
	"brightness2": 50
	}

# Brightness array used to store potential multiple brightnesses
# So colors can be updated accordingly
# 10 0.1's just so I don't have to adjust size each time I add a brightness slider
brightness_arr = [0.1] * 10

def hex_to_grb(hex):
	# Courtesy of: https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
	# Modified to return grb, not rgb
	hex = hex.lstrip('#')	# Removes initial hash
	rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))	# Finds rgb values
	grb = (rgb[1], rgb[0], rgb[2])	# Trades r & g values to create grb tuple
	return grb

color_arr = [hex_to_grb("#FF4614")] * 10

# Amount of colors dictionary
effect_color_amounts = {
	"Off": 1,
	"Single color": 1,
	"Static alternating colors": 2,
	"Animated alternating colors": 2,
	"Random": 1
}

# TODO: Test with another looping effect and running them back to back
def looping_effects_analyzer(looping_effect_queue, looping_event, static_effect_queue, color_arr, brightness_arr):
	# This wait blocks the below code until a selected looping effect triggers it to run
	looping_event.wait()

	# This while loop keeps the thread alive when it is idle
	# Otherwise when the looping event is set to false, it will exit out of its while loop in the effect function
		# Return to this thread function, see there are no more commands
			# And it will die, not to be revived
	# So in other words, don't delete this while loop lol
	while True:
		looping_effect_name = looping_effect_queue.get()

		if looping_effect_name == "Random":
			random_colors(brightness_arr, looping_effect_queue, static_effect_queue)

		if looping_effect_name == "Animated alternating colors":
			animated_alternating_colors(color_arr, looping_effect_queue, static_effect_queue)

looping_effects = ["Random", "Animated alternating colors"]
looping_event = threading.Event()
looping_effect_queue = queue.Queue()
static_effect_queue = queue.Queue()
thread = threading.Thread(target = looping_effects_analyzer, name = "looping thread", args = (looping_effect_queue, looping_event, static_effect_queue, color_arr, brightness_arr,))

@app.route("/", methods = ["GET", "POST"])
def action():
	if request.method == 'POST':
		# Copies form values to be used outside this function (in getting values)
			# Form data is local to the app route, so by copying it it can be exported
		global form_data
		form_data = request.form.copy()

		global effect
		effect = get_value("effect")
		
		# This is a workaround since the checkbox unchecked won't POST data
			# aka wont show up in request dict and will throw an error
		# SO KEEP THIS AS REQUEST.FORM, NOT GET_VALUE
		global has_mult_brightnesses
		try:
			# Converts string "True" to boolean True
			has_mult_brightnesses = (request.form["mult brightnesses checkbox"] == "True")
		except:
			has_mult_brightnesses = False

		# This is to debug what keys are actually posted currently to the form
		#print(request.form)

		get_colors()
		get_brightnesses()
		apply_brightnesses()
		do_effect()

		if effect in looping_effects:
			static_effect_queue.queue.clear()
			looping_effect_queue.put_nowait(effect)
			looping_event.set()
		else:
			looping_event.clear()
			static_effect_queue.put(effect)


		return render_template('index.html')
	
	else:
		return render_template('index.html')

# This is a workaround for form elements that haven't yet been initialized by a form submit causing a key error
def get_value(element_name):
	val = 0
	try:
		val = form_data[element_name]
	except Exception as e:
		val = default_form_values[element_name]

	return val

def get_colors():
	for i in range(effect_color_amounts[effect]):
		col = "color"
		col += str(i)
		color_arr[i] = hex_to_grb(get_value(col))

def get_brightnesses():
	if has_mult_brightnesses:
		for i in range(effect_color_amounts[effect]):
			b = "brightness"
			b += str(i)
			brightness_arr[i] = float(get_value(b))/100
	else:
		brightness_arr[0] = float(get_value("brightness0"))/100

def apply_brightnesses():
	for i in range(effect_color_amounts[effect]):

		if has_mult_brightnesses:
			b_index = i
		else:
			b_index = 0

		g = color_arr[i][0] * brightness_arr[b_index]
		r = color_arr[i][1] * brightness_arr[b_index]
		b = color_arr[i][2] * brightness_arr[b_index]
		color_arr[i] = (g, r, b)

def do_effect():
	if effect == "Single color":
		single_color(color_arr[0])

	if effect == "Off":
		off()

	if effect == "Static alternating colors":
		alternating_colors(color_arr)

if __name__ == "__main__":
	thread.start()
	app.run(host='0.0.0.0', port=80, debug = True, threaded = True)