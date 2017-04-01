#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sqlite3
import os.path
from TemperatureSensorProvider import TemperatureSensorProvider
from Logger import Logger
import RPi.GPIO as GPIO
import time

conn = sqlite3.connect("/data/websites/greenhouse.local/db/greenhouse.db")
curs=conn.cursor()

temperatureSensors = TemperatureSensorProvider(conn)
logger = Logger(conn)

def readSensors():
    
    for sensor in temperatureSensors.getSensors():
        print "Sensor: ", sensor.name
        print "Temperature: ", sensor.temperature , "°C (max: ", sensor.max ,"°C)\n"
                
        if sensor.temperature > sensor.max:
            logger.log("Sensor " + sensor.name + " is above max value\n")
            runFan()
            break

def runFan():
	fanRunTime = 300

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(18,GPIO.OUT)
        
        message = "Starting fan, running for " + str(fanRunTime) + " seconds"
	logger.log(message)
	GPIO.output(18, GPIO.HIGH)
	time.sleep(fanRunTime)
	logger.log("Stopping fan")
	GPIO.output(18, GPIO.LOW)

readSensors()
conn.close()

