#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import sqlite3
import os.path
import datetime
import time
from Logger import Logger

conn = sqlite3.connect("/data/websites/greenhouse.local/db/greenhouse.db")
curs=conn.cursor()
logger = Logger(conn)

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 22
GPIO_ECHO    = 24

print "Checking water level"

GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

GPIO.output(GPIO_TRIGGER, False)

time.sleep(0.5)

def readSensors():
	curs.execute ("SELECT * from Sensors where SensorType = 'waterlevel'")

	for reading in curs.fetchall():
		sensorId = reading[1]
		sensorName = reading[2]
		sensorMin = reading[4]
		sensorMax = reading[5]

		numberOfPings = 10
		pingInterval = 1
		result = 0

		for num in range(0, numberOfPings):
			print "Ping " + str(num + 1)

			GPIO.output(GPIO_TRIGGER, True)
			time.sleep(0.001)
			GPIO.output(GPIO_TRIGGER, False)
			start = time.time()

			while GPIO.input(GPIO_ECHO)==0:
				start = time.time()

			while GPIO.input(GPIO_ECHO)==1:
				stop = time.time()

			elapsed = stop-start

			distance = (elapsed * 34300) / 2
			
			result = result + float(distance)
			print distance

			time.sleep(pingInterval)


		if result < sensorMin:
			logger.log("Water level low")
		
		
		endResult = result / numberOfPings

		if result < sensorMin:
                        logger.log("Water level low")
		
		print "Result: " + str(endResult)
		print (sensorMin/endResult) *100
		logger.SaveSensorData(sensorId, sensorName, (sensorMin / endResult) - 1)

readSensors()
GPIO.cleanup()
