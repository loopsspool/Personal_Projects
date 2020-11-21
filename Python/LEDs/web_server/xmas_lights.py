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
	print("Got here!")
	#print(request.form["effects"], flush=True)
    # Reads action and acts
	effect = request.form["effects"]
	if effect == "on":
		pixels.fill((255, 0, 0))
	if effect == "off":
		pixels.fill((0, 0, 0))
    #if action == "effect":
    #    exec(open("test2.py").read())
		     
	#ledRedSts = GPIO.input(ledRed)
   
	templateData = {
              #'led_status' : led_status
	}

	return render_template('index.html', **templateData)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True) 