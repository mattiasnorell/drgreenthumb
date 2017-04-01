class TemperatureSensor:
	def __init__(self, id, serialNumber, name, type, temperature, min, max):
		self.id = id
		self.serialNumber = serialNumber
		self.name = name
		self.type = type
		self.temperature = temperature
		self.min = min
		self.max = max