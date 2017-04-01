#!/usr/bin/env python
# -*- coding: utf-8 -*- 

class Logger:
	
	def __init__(self, connection):
		self.connection = connection

	def log(self, val):
		# Log to database
		print val
		curs = self.connection.cursor()
		curs.execute ("INSERT INTO Logs (DateTime, Message) VALUES(datetime('now','localtime'),?)",(val,))
		self.connection.commit()

	def SaveSensorData(self, sensorId, sensorName, value):
		curs = self.connection.cursor()
		curs.execute ("INSERT INTO SensorData (SensorId,Datetime, SensorValue) VALUES(?,datetime('now','localtime'),?)",(sensorId, value))
		self.connection.commit()