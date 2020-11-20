import light_effects
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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
	
@app.route("/<action>")
def action(action):
    # Reads action and acts
	if action == "on":
		GPIO.output(actuator, GPIO.HIGH)
	if action == "off":
		GPIO.output(actuator, GPIO.LOW)
    #if action == "effect":
    #    exec(open("test2.py").read())
		     
	#ledRedSts = GPIO.input(ledRed)
   
	templateData = {
              #'led_status' : led_status
	}

	return render_template('index.html', **templateData)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True) 