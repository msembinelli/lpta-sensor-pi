#!/usr/bin/env python
#import time
import os
import RPi.GPIO as GPIO
#import eeml
 
GPIO.setmode(GPIO.BCM)
DEBUG = 0
LOGGER = 1
 
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)
 
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low
 
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:   
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
 
        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1
 
        GPIO.output(cspin, True)
 
        adcout /= 2       # first bit is 'null' so drop it
        return adcout

def sensorFunc():
 
	# change these as desired - they're the pins connected from the
	# SPI port on the ADC to the Cobbler
	SPICLK = 18
	SPIMISO = 23
	SPIMOSI = 24
	SPICS = 25
	POLL_TIME = 10
 
	# set up the SPI interface pins
	GPIO.setup(SPIMOSI, GPIO.OUT)
	GPIO.setup(SPIMISO, GPIO.IN)
	GPIO.setup(SPICLK, GPIO.OUT)
	GPIO.setup(SPICS, GPIO.OUT)
 
	# COSM variables. The API_KEY and FEED are specific to your COSM account and must be changed 
	#API_KEY = '5RNOO3ShYJxYiq2V2sgSRtz3112SAKxFQjNDQmNXc0RScz0g'
	#FEED = 68872
#	API_KEY = '5o99TlXGJ02f0kPWzS1Erb822VNiYYvleurjm2PwHXFyyAsR'
#	FEED = 984389260
 
#	API_URL = '/v2/feeds/{feednum}.xml' .format(feednum = FEED)
 
	# temperature sensor connected channel 0 of mcp3008
	adcnum = 0
 
	# read the analog pin (temperature sensor LM35)
	read_adc0 = readadc(adcnum, SPICLK, SPIMOSI, SPIMISO, SPICS)
 
	# convert analog reading to millivolts = ADC * ( 3300 / 1024 )
	millivolts = read_adc0 * ( 3300.0 / 1024.0)
 
# 10 mv per degree 
	temp_C = ((millivolts - 100.0) / 10.0) - 40.0
 
# convert celsius to fahrenheit 
	#temp_F = ( temp_C * 9.0 / 5.0 ) + 32
 
# remove decimal point from millivolts
	millivolts = "%d" % millivolts
 
# show only one decimal place for temprature and voltage readings
	temp_C = "%.1f" % temp_C
	#temp_F = "%.1f" % temp_F
 
	if DEBUG:
		print "%s - Temperature: %s C" % (time.ctime(time.time()), temp_C)
        	#print("temp_F:\t\t", temp_F)
		print "----------"
 
	if LOGGER:
        # open up your cosm feed
 #       	pac = eeml.Pachube(API_URL, API_KEY)
 
        #send celsius data
  #      	pac.update([eeml.Data(0, temp_C, unit=eeml.Celsius())])
 
                #send fahrenheit data
        #pac.update([eeml.Data(1, temp_F, unit=eeml.Fahrenheit())])
 
        # send data to cosm
   #     	pac.put()
	#return
		return float(temp_C)
 
# hang out and do nothing for 10 seconds, avoid flooding cosm
#	time.sleep(POLL_TIME)

if __name__ == '__main__':
	sensorFunc()
