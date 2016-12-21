#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
import thread
import TMP_SCRIPT
import LIGHT_SCRIPT
import math
from time import sleep, strftime
import PRESSURE_SCRIPT
from datetime import datetime
import eeml
 
# COSM variables.
API_KEY = '5o99TlXGJ02f0kPWzS1Erb822VNiYYvleurjm2PwHXFyyAsR'
FEED = 984389260 
API_URL = '/v2/feeds/{feednum}.xml' .format(feednum = FEED)
 

GLOBAL_TMP = 0.0
GLOBAL_LIGHT = 0.0
GLOBAL_PRESSURE = 0.0
GLOBAL_ALTITUDE = 0.0

#XIVELY_DATA_BUFFER = []
BufferCount = 0

lcd = Adafruit_CharLCD()
lcd.begin(20,4)

if __name__ == '__main__':

	print "\n"
	print "Welcome to Matt's SensorNet"
	print "---------------------------------------------------------"
	print "....monitoring..."

	while True:
		GLOBAL_TMP = TMP_SCRIPT.sensorFunc()
		GLOBAL_LIGHT = LIGHT_SCRIPT.sensorFunc()
		GLOBAL_PRESSURE = PRESSURE_SCRIPT.sensorFunc()

		lcd.clear()
		lcd.message('TEMP:     %.1f   C\2LIGHT:    %.1f  lux\3PRESSURE: %.1f   kPa\4ALTITUDE: %.1f m' % (GLOBAL_TMP, GLOBAL_LIGHT, GLOBAL_PRESSURE,math.log(float(GLOBAL_PRESSURE)/101.325)*(-7000)))
		sleep(2)
		
		if BufferCount == 5:
			# open up your cosm feed
        		pac = eeml.Pachube(API_URL, API_KEY)
 
			# prepare altitude for xively
			GLOBAL_ALTITUDE = math.log(float(GLOBAL_PRESSURE)/101.325)*(-7000)

        		#send lux data
			pac.update([eeml.Data(0, GLOBAL_TMP, unit=eeml.Celsius())])
        		pac.update([eeml.Data(1, GLOBAL_LIGHT, unit=eeml.Unit('LuminousFlux', type='basicSI', symbol='lx'))])
	 		pac.update([eeml.Data(2, GLOBAL_PRESSURE, unit=eeml.Unit(name='kilopascal', type='derivedSI', symbol='kPa'))])
			pac.update([eeml.Data(3, GLOBAL_ALTITUDE, unit=eeml.Unit(name='altitude', type='derivedSI', symbol='m'))])

        		# send data to cosm
        		pac.put()
 			
			BufferCount = 0
			# hang out and do nothing for 10 seconds, avoid flooding cosm
#			sleep(5)
		
		BufferCount += 1
