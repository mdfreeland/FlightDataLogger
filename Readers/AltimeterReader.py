from lib.Adafruit_BME280 import *

class AltimeterReader:
    def __init__(self):
        self.sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

    def getReading(self):
        degrees = self.sensor.read_temperature()
        pascals = self.sensor.read_pressure()
        hectopascals = pascals / 100
        return { 'Temperature (C)': '{0:0.3f}'.format(degrees), 'Pressure (hPa)': '{0:0.2f}'.format(hectopascals) }
