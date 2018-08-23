from lib.Adafruit_BME280 import *
import logging

class AltimeterReader:
    def __init__(self):
        self.logger = logging.getLogger('FlightDataLogger.AltimeterReader')
        self.logger.info('Altimeter Reader initializing...')
        self.sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

    def getReading(self):
        try:
            degrees = self.sensor.read_temperature()
            self.logger.info('Temperature reading received: ' + '{0:0.3f}'.format(degrees))

            pascals = self.sensor.read_pressure()
            hectopascals = pascals / 100
            self.logger.info('Pressure reading received: ' + '{0:0.2f}'.format(hectopascals))
        except (KeyboardInterrupt, SystemExit):
            # Don't prevent ctrl-c from terminating the program
            raise
        except Exception:
            self.logger.exception('Failed to read temperature/pressure due to exception:')

        return { 'Temperature (C)': '{0:0.3f}'.format(degrees), 'Pressure (hPa)': '{0:0.2f}'.format(hectopascals) }
