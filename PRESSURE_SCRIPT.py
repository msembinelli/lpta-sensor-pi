#!/usr/bin/python

#import time
import math
import os
#import eeml
from MPL115A2_class import MPL115A2

DEBUG = 0
LOGGER = 1

#API_KEY = '5o99TlXGJ02f0kPWzS1Erb822VNiYYvleurjm2PwHXFyyAsR'
#FEED = 984389260
#API_URL = '/v2/feeds/{feednum}.xml' .format(feednum = FEED)

mp = MPL115A2()

def sensorFunc():
    rList = mp.getPT()
    #Temperature is inaccurate compared to TMP36
    #print "%s - Temperature: %03.2f C" % (time.ctime(time.time()),rList[1])
    #rList[0] = "%d" % float(rList[int(0)])
    Pressure = "%d" % float(rList[0])
    Pressure = "%.1f" % float(Pressure)
    Altitude = math.log(float(Pressure)/101.325)*(-7000)
    Altitude = "%d" % float(Altitude)
    Altitude = "%.1f" % float(Altitude)	
    if DEBUG:
    	print "%s - Pressure: %03.2f kPa" % (time.ctime(time.time()), rList[0])
    	print "----------"
    	print "%s - Altitude: %03.2f m" % (time.ctime(time.time()), (math.log(rList[0]/101.325)*-7000))
    	print "----------"
    	print "\n\n"
    if LOGGER:
#	pac = eeml.Pachube(API_URL, API_KEY)
#	pac.update([eeml.Data(2, float(Pressure), unit=eeml.Unit(name='kilopascal', type='derivedSI', symbol='kPa'))])
#	pac.update([eeml.Data(3, float(Altitude), unit=eeml.Unit(name='altitude', type='derivedSI', symbol='m'))])
#	pac.put()
	return float(Pressure)

 #   time.sleep(12)

if __name__ == '__main__':
	
	sensorFunc()
