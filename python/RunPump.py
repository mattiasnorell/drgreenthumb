#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import RPi.GPIO as GPIO
import sqlite3
import time
from Logger import Logger
from Sensors import WaterLevel

conn = sqlite3.connect("/data/websites/greenhouse.local/db/greenhouse.db")
curs=conn.cursor()

logger = Logger(conn)
sensor = WaterLevel()

timeToPump = 2

def checkWaterLevel():
    return sensor.GetSensorValue()

def runPump():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(23,GPIO.OUT)
    
    isWaterLevelEnough = checkWaterLevel()

    if(isWaterLevelEnough):
        logger.log("Starting pump, run for " + str(timeToPump) + " sec")
        GPIO.output(23, GPIO.HIGH)
        time.sleep(timeToPump)
        logger.log("Stopping pump")
        GPIO.output(23, GPIO.LOW)
    else:
        logger.log("Not enough water to run pump")
    
runPump()
