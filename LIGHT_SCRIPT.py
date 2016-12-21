#!/usr/bin/env python
#import time
import os
import RPi.GPIO as GPIO
#import eeml
import math
 
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
 
# set up the SPI interface pins
	GPIO.setup(SPIMOSI, GPIO.OUT)
	GPIO.setup(SPIMISO, GPIO.IN)
	GPIO.setup(SPICLK, GPIO.OUT)
	GPIO.setup(SPICS, GPIO.OUT)
 
# COSM variables. The API_KEY and FEED are specific to your COSM account and must be changed 

#	API_KEY = '5o99TlXGJ02f0kPWzS1Erb822VNiYYvleurjm2PwHXFyyAsR'
#	FEED = 984389260
 
#	API_URL = '/v2/feeds/{feednum}.xml' .format(feednum = FEED)
 
# light sensor connected channel 1 of mcp3008
	adcnum = 1
 
# read the analog pin (temperature sensor LM35)
	read_adc1 = readadc(adcnum, SPICLK, SPIMOSI, SPIMISO, SPICS)
 
# convert analog reading to lux
	lux = read_adc1 * ( 5.0 / 1024.0)
	lux = math.pow(10,lux)
	 
# remove decimal point from lux
	lux = "%d" % float(lux)
 
# show only one decimal place for lux readings
	lux = "%.1f" % float(lux)

	if DEBUG:
		print "%s - Ambient Light: %s lx" % (time.ctime(time.time()),lux)
        	print "----------"
 
	if LOGGER:
        # open up your cosm feed
   #     	pac = eeml.Pachube(API_URL, API_KEY)
 
        #send lux data
  #      	pac.update([eeml.Data(1, lux, unit=eeml.Unit('LuminousFlux', type='basicSI', symbol='lx'))])
 
        # send data to cosm
 #       	pac.put()
	# return value to master thread
	
		return float(lux)
 
# hang out and do nothing for 10 seconds, avoid flooding cosm
#	time.sleep(10)

if __name__ == '__main__':

	sensorFunc()
