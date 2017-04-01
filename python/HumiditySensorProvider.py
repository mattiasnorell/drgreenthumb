#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from HumiditySensor import HumiditySensor
import os.path
import Adafruit_DHT

class HumiditySensorProvider:
	
	def __init__(self, connection):
		self.connection = connection

	def getSensorValue(self, serialNumber):
		sensor = Adafruit_DHT.DHT22
		humidity, temperature = Adafruit_DHT.read_retry(sensor, serialNumber)

		return humidity

	def getSensors(self):
		return self.readSensors()

	def readSensors(self):
		sensors = []

		curs = self.connection.cursor()

		curs.execute ("""SELECT * from Sensors where SensorType = 'humidity'""")

		for reading in curs.fetchall():
			sensorId = reading[0]
			sensorSerialNumber = str(reading[1])
			sensorName = str(reading[2])
			sensorType = str(reading[3])
			sensorMinValue = reading[4]
			sensorMaxValue = reading[5]

			value = self.getSensorValue(sensorSerialNumber)

			with self.connection:
				if sensorType == "humidity":
					#def __init__(self, id, serialNumber, name, type, temperature, min, max):
					sensor = HumiditySensor(sensorId, sensorSerialNumber, sensorName, sensorType, value, sensorMinValue, sensorMaxValue)
					sensors.append(sensor)

		return sensors
