import serial
import csv
import chardet
from time import sleep
import logging

class RadiometryReader:
    columns = ['Detector Type', 'Serial Number', 'Record Date', 'Record Time', 'Recorded Value', 'Units', 'Extra Unit Digits', 'Flags', 'Calibration Due Date']
    
    def __init__(self):
        self.logger = logging.getLogger('FlightDataLogger.RadiometryReader')
        self.logger.info('Radiometry Reader initializing...')
        
        self.radiometer = serial.Serial('/dev/ttyUSB0', 2400, timeout=1)
        
        # Send p character to initialize data transfer from radiometer
        self.radiometer.write(b'p')

    def clearRadiometerInternalDataStorage(self):
        self.logger.info('Sending the command to the radiometer to clear all UV readings from its internal storage')
        # Clear UV readings stored in the Solar Light Radiometer internal storage
        self.radiometer.write(b'\x03')
        sleep(1)
        self.radiometer.write(b'y')
        sleep(1)
        self.radiometer.readline()

    def getReading(self):
        # Get the reading and decode the byte array to a string
        try:
            reading = self.radiometer.readline().decode('iso8859-15').replace('\0', '')
        except (KeyboardInterrupt, SystemExit):
            # Don't prevent ctrl-c from terminating the program
            raise
        except Exception as e:
            print(e)
            self.logger.exception('Failed to decode radiometry reading byte array due to exception:')
            return None
        
        if len(reading) == 0:
            return None
        
        self.logger.info('UV reading received: ' + reading)

        try:
            data =list(csv.DictReader(reading.splitlines(), self.columns, dialect='excel'))[0]
        except (KeyboardInterrupt, SystemExit):
            # Don't prevent ctrl-c from terminating the program
            raise
        except Exception as e:
            print(e)
            self.logger.exception('Failed to parse radiometry reading csv row due to exception:')
            return self.getEmptyReading()

        return data

    def getEmptyReading(self):
        return {key: '' for key in self.columns}

    def stop(self):
        self.radiometer.close()