import board
import neopixel
import light_effects
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# number of LEDs
num_of_leds = 150

# initialize LED strip
pixels = neopixel.NeoPixel(board.D18, num_of_leds)

#define LED GPIO pin
leds = 18

#initialize GPIO status variables
led_status = "Off"

# Define led pin as output
GPIO.setup(leds, GPIO.OUT)   

@app.route("/")
def index():
	templateData = {
              'title' : 'Xmas lights!',
              #'led_status' : led_status
    }
	return render_template('index.html', **templateData)
	
@app.route("/", methods = ["GET", "POST"])
def action():
    # Reads action and acts
	effect = request.form["effects"]
	brightness = float(request.form["brightness"])/100
	color = hex_to_rgb(request.form["color"])

	if effect == "on":
		# Color[1], then color[0] because my lights are grb not rgb
		pixels.fill((color[1] * brightness, color[0] * brightness, color[2] * brightness))
	if effect == "off":
		pixels.fill((0, 0, 0))
    #if action == "effect":
    #    exec(open("test2.py").read())
		     
	#ledRedSts = GPIO.input(ledRed)
   
	templateData = {
              #'led_status' : led_status
	}

	return render_template('index.html', **templateData)

def hex_to_rgb(hex):
	# Courtesy of: https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
	hex = hex.lstrip('#')
	return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True) 