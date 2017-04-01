#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sqlite3
import os.path
from HumiditySensorProvider import HumiditySensorProvider
from Logger import Logger
import RPi.GPIO as GPIO
import time

conn = sqlite3.connect("/data/websites/greenhouse.local/db/greenhouse.db")
curs=conn.cursor()

sensors = HumiditySensorProvider(conn)
logger = Logger(conn)

def saveValue(sensorId, sensorName, value):
    print sensorId
    print sensorName
    print value
    curs.execute ("INSERT INTO SensorData (SensorId, Datetime, SensorValue) VALUES(?,datetime('now','localtime'),?)",(sensorId, value))
    conn.commit()

def readSensors():
    
    for sensor in sensors.getSensors():
        print "Sensor: ", sensor.name
        print "Humidity: ", sensor.value , "°C (max: ", sensor.max ,"°C)\n"

        saveValue(sensor.id, sensor.name, sensor.value)

        if sensor.value > sensor.max:
            logger.log("Sensor " + sensor.name + " is above max value\n")
            break

readSensors()
conn.close()
