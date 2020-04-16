#-*- coding: utf-8 -*-
import RPi.GPIO as GPIO 
import time
from datetime import datetime
import sys
import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
tank_min = 130
well_min = 250
watering_hour = "02:43 PM"

class gtc:
	def __init__(self):
		print('Initialisation de la Gestion Technique centralisée')
		time.sleep(0.5)

	def cleanup(self):
		GPIO.cleanup()

	class relay:

		def __init__(self, gpio):
			self.gpio = gpio
			print('Initialisation du relais GPIO : {}'.format(self.gpio))
			GPIO.setup(self.gpio, GPIO.OUT)
			self.on()
			time.sleep(0.5)
			self.off()
			time.sleep(0.5)
			self.type = "relay"

		def on(self):
			GPIO.output(self.gpio, GPIO.HIGH)
		
		def off(self):
			GPIO.output(self.gpio, GPIO.LOW)
		
		def status(self):
			return GPIO.input(self.gpio)

	class ultrasonic:

		def __init__(self, gpio_trigger, gpio_echo):
			self.gpio_trigger = gpio_trigger
			self.gpio_echo = gpio_echo
			print('Initialisation du capteur ultrason GPIO : ')
			print('\t Trigger GPIO \t: {}'.format(self.gpio_trigger))
			print('\t Echo GPIO \t: {}'.format(self.gpio_echo))
			GPIO.setup(self.gpio_trigger,GPIO.OUT)
			GPIO.setup(self.gpio_echo,GPIO.IN)
			depth_per = 100 - ((self.average_depth() / 150) * 100)
			print("Reservoir rempli à {} %".format(int(depth_per)))
			time.sleep(0.5)

		def instant_depth(self):
			GPIO.output(self.gpio_trigger, GPIO.LOW)
			time.sleep(0.5)
			GPIO.output(self.gpio_trigger, GPIO.HIGH) # set TRIGGER to HIGH
			time.sleep(0.00001) # wait 10 microseconds
			GPIO.output(self.gpio_trigger, GPIO.LOW) # set TRIGGER to LOW
			start = time.time()
			while GPIO.input(self.gpio_echo)==0:
				start = time.time()
			# Assign the actual time to stop variable until the ECHO goes back from HIGH to LOW
			while GPIO.input(GPIO_ECHO)==1:
				stop = time.time()
			# Calculate the time it took the wave to travel there and back
			measuredTime = stop - start
			# Calculate the travel distance by multiplying the measured time by speed of sound
			distanceBothWays = measuredTime * 33112 # cm/s in 20 degrees Celsius
			# Divide the distance by 2 to get the actual distance from sensor to obstacle
			depth = distanceBothWays / 2
			return depth

		def average_depth(self):
			i = 0
			depth_sum = 0
			depth = 0
			GPIO.output(self.gpio_trigger, GPIO.LOW)
			time.sleep(0.5)
			while (i < 10):
				GPIO.output(self.gpio_trigger, GPIO.HIGH) # set TRIGGER to HIGH
				time.sleep(0.00001) # wait 10 microseconds
				GPIO.output(self.gpio_trigger, GPIO.LOW) # set TRIGGER to LOW
				start = time.time()
				while GPIO.input(self.gpio_echo)==0:
					start = time.time()
				# Assign the actual time to stop variable until the ECHO goes back from HIGH to LOW
				while GPIO.input(self.gpio_echo)==1:
					stop = time.time()
				# Calculate the time it took the wave to travel there and back
				measuredTime = stop - start
				# Calculate the travel distance by multiplying the measured time by speed of sound
				distanceBothWays = measuredTime * 33112 # cm/s in 20 degrees Celsius
				# Divide the distance by 2 to get the actual distance from sensor to obstacle
				depth = distanceBothWays / 2
				if (depth != 0):
					depth_sum = depth_sum + depth
					i+=1
			average_depth = (depth_sum / i)
			return depth

		def check_tank(self):
			depth_per = 100 - ((self.average_depth() / 150) * 100)
			if (depth_per > 20):
				#print("Reservoir d'eau rempli à {} %".format(depth_per))
				return True
			else:
				return False

	class rain:
		def __init__(self, gpio):
			self.gpio = gpio
			print('Initialisation du capteur de pluie/arrosage GPIO : {}'.format(self.gpio))
			time.sleep(0.5)
			GPIO.setup(self.gpio, GPIO.IN)
		
		def status(self):
			return GPIO.input(self.gpio)
			
		def check_rain(self):
			if (self.status() == 1):
				return True
			else:
				return False