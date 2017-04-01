#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sqlite3
import os.path
from TemperatureSensorProvider import TemperatureSensorProvider

conn = sqlite3.connect("/data/websites/greenhouse.local/db/greenhouse.db")
curs=conn.cursor()

def saveTemperature(sensorId, sensorName, temp):
    curs.execute ("INSERT INTO SensorData (SensorId,Datetime, SensorValue) VALUES(?,datetime('now','localtime'),?)",(sensorId, temp))
    conn.commit()

def readSensors():
    temperatureSensors = TemperatureSensorProvider(conn)

    for sensor in temperatureSensors.getSensors():
        print "Sensor: ", sensor.name
        print "Temperature: ", sensor.temperature , "°C\n"
        saveTemperature(sensor.id, sensor.name, sensor.temperature)
                
readSensors()
conn.close()