import board
import neopixel
import time
import random
from light_effects import *
from flask import Flask, render_template, request
import threading
import queue
import os # For CPU temp

# TODO: Move all functions to main_functions.py and import them
	# Just for cleanliness' sake

app = Flask(__name__, template_folder = '', static_folder = '', static_url_path = '')

# Workaround for form elements not yet being initialized into form.request
# Won't work with HTML onload because all code files are validated first
# So there was still an error in python refrencing a bad key in form.request
# So default form values are used in a try except block until a form value is changed
# At which point the whole form submits and the elements will be loaded into form.request
default_form_values = {
	"effect": "Color",
	"amount of colors": 1,
	"color0": "#FF4614",
	"color1": "#FF4614",
	"color2": "#FF4614",
	"color3": "#FF4614",
	"color4": "#FF4614",
	"color5": "#FF4614",
	"color6": "#FF4614",
	"color7": "#FF4614",
	"color8": "#FF4614",
	"color9": "#FF4614",
	"mult color style": "alternating",
	"block size": 1,
	"mult brightnesses checkbox": False,
	"brightness0": 50,
	"brightness1": 50,
	"brightness2": 50,
	"brightness3": 50,
	"brightness4": 50,
	"brightness5": 50,
	"brightness6": 50,
	"brightness7": 50,
	"brightness8": 50,
	"brightness9": 50,
	"animated speed slider": 50
	}

# Brightness array used to store potential multiple brightnesses
# So colors can be updated accordingly
brightness_arr = [0.1] * 10

def hex_to_grb(hex):
	# Courtesy of: https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
	# Modified to return grb, not rgb
	hex = hex.lstrip('#')	# Removes initial hash
	rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))	# Finds rgb values
	grb = (rgb[1], rgb[0], rgb[2])	# Trades r & g values to create grb tuple
	return grb

color_arr = [hex_to_grb("#FF4614")] * 10

def looping_effects_analyzer(looping_event, queue_dict, color_arr, brightness_arr):
	# This wait blocks the below code until a selected looping effect triggers it to run
	looping_event.wait()

	# This while loop keeps the thread alive when it is idle
	# Otherwise when the looping event is set to false, it will exit out of its while loop in the effect function
		# Return to this thread function, see there are no more commands
			# And it will die, not to be revived
	# So in other words, don't delete this while loop lol
	while True:
		looping_effect_name = queue_dict["looping effect queue"].get()

		if looping_effect_name == "Random":
			random_colors(brightness_arr, queue_dict)

		if looping_effect_name == "Animated alternating colors":
			animated_alternating_colors(color_arr, queue_dict)

		if looping_effect_name == "Twinkle":
			twinkle(color_arr, queue_dict)

looping_effects = ["Random", "Animated alternating colors", "Twinkle"]
looping_event = threading.Event()
looping_effect_queue = queue.Queue()
static_effect_queue = queue.Queue()
amount_of_colors_queue = queue.Queue()
animated_effect_speed_queue = queue.Queue()
block_size_queue = queue.Queue()
queue_dict = {
	"looping effect queue": looping_effect_queue,
	"static effect queue": static_effect_queue,
	"amount of colors queue": amount_of_colors_queue,
	"animated effect speed queue": animated_effect_speed_queue,
	"block size queue": block_size_queue
}
prev_color_amount = default_form_values["amount of colors"]
prev_effect_speed = default_form_values["animated speed slider"]
prev_mult_color_style = default_form_values["mult color style"]
prev_block_size = default_form_values["block size"]
thread = threading.Thread(target = looping_effects_analyzer, name = "looping thread", args = (looping_event, queue_dict, color_arr, brightness_arr,))

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

		# Checking if certain elements have changed to notify the animated effect thread
		current_effect_speed = get_value("animated speed slider")
		global prev_effect_speed
		if not current_effect_speed == prev_effect_speed:
			animated_effect_speed_queue.put_nowait(current_effect_speed)
			prev_effect_speed = current_effect_speed

		current_color_amount = get_value("amount of colors")
		global prev_color_amount
		if not current_color_amount == prev_color_amount:
			amount_of_colors_queue.queue.clear()
			amount_of_colors_queue.put_nowait(current_color_amount)
			prev_color_amount = current_color_amount

		current_mult_color_style = get_value("mult color style")
		current_block_size = get_value("block size")
		global prev_mult_color_style
		global prev_block_size
		# If radio buttons have changed
		if not current_mult_color_style == prev_mult_color_style:
			# To alternating, block size = 1
			if current_mult_color_style == "alternating":
				prev_block_size = 1
			# To block, block size = block
			elif current_mult_color_style == "block":
				prev_block_size = current_block_size

			block_size_queue.queue.clear()
			block_size_queue.put_nowait(prev_block_size)
			prev_mult_color_style = current_mult_color_style

		# Or if the radio was still on the block selection but block size changed
		elif current_mult_color_style == prev_mult_color_style and current_mult_color_style == "block" and not current_block_size == prev_block_size:
			block_size_queue.queue.clear()
			block_size_queue.put_nowait(current_block_size)
			prev_block_size = current_block_size


		pi_temp = get_temp()
		return render_template('index.html', temp = pi_temp)
	
	else:
		pi_temp = get_temp()
		return render_template('index.html', temp = pi_temp)

# This is a workaround for form elements that haven't yet been initialized by a form submit causing a key error
def get_value(element_name):
	val = 0
	try:
		val = form_data[element_name]
	except Exception as e:
		val = default_form_values[element_name]

	return val

def get_colors():
	for i in range(int(get_value("amount of colors"))):
		col = "color"
		col += str(i)
		color_arr[i] = hex_to_grb(get_value(col))

def get_brightnesses():
	if has_mult_brightnesses:
		for i in range(int(get_value("amount of colors"))):
			b = "brightness"
			b += str(i)
			brightness_arr[i] = float(get_value(b))/100
	else:
		brightness_arr[0] = float(get_value("brightness0"))/100

def apply_brightnesses():
	for i in range(int(get_value("amount of colors"))):

		if has_mult_brightnesses:
			b_index = i
		else:
			b_index = 0

		g = color_arr[i][0] * brightness_arr[b_index]
		r = color_arr[i][1] * brightness_arr[b_index]
		b = color_arr[i][2] * brightness_arr[b_index]
		color_arr[i] = (g, r, b)

def do_effect():
	if effect == "Color":
		color(color_arr, int(get_value("amount of colors")), int(get_value("block size")))

	if effect == "Off":
		off()

def get_temp():
	temp = os.popen('vcgencmd measure_temp').readline()
	return(temp.replace("temp=", "").replace("/n",""))

if __name__ == "__main__":
	thread.start()
	app.run(host='0.0.0.0', port=80, debug = True, threaded = True)