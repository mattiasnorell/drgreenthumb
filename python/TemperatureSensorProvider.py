#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from TemperatureSensor import TemperatureSensor
import os.path

class TemperatureSensorProvider:
	
	def __init__(self, connection):
		self.connection = connection

	def parseTemperature(self, input):
		secondline = input.split("\n")[1]
		temperaturedata = secondline.split(" ")[9]
		temperature = float(temperaturedata[2:])
		return temperature / 1000   

	def getSensorConfigFile (self, sensorId):
		sensorPath = "/sys/bus/w1/devices/"+ sensorId +"/w1_slave"
		if os.path.isfile(sensorPath): 
			tfile = open(sensorPath)
			text = tfile.read()
			tfile.close()
			return text
		return ""
	
	def getSensors(self):
		return self.readSensors()

	def readSensors(self):
		sensors = []

		curs = self.connection.cursor()

		curs.execute ("""SELECT * from Sensors where SensorType = 'temp'""")

		for reading in curs.fetchall():
			sensorId = reading[0]
			sensorSerialNumber = str(reading[1])
			sensorName = str(reading[2])
			sensorType = str(reading[3])
			sensorMinValue = reading[4]
			sensorMaxValue = reading[5]
			text = self.getSensorConfigFile(sensorSerialNumber)  

			if text == "":
				print "Sensor not found: ", sensorName, ", S/N:", sensorSerialNumber
				continue

			temp = self.parseTemperature(text)

			with self.connection:
				if sensorType == "temp":
					#def __init__(self, id, serialNumber, name, type, temperature, min, max):
					sensor = TemperatureSensor(sensorId, sensorSerialNumber, sensorName, sensorType, temp, sensorMinValue, sensorMaxValue)
					sensors.append(sensor)

		return sensors
