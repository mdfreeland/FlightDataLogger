import serial
import csv
import chardet
from time import sleep

class RadiometryReader:
    columns = ['Detector Type', 'Serial Number', 'Record Date', 'Record Time', 'Recorded Value', 'Units', 'Extra Unit Digits', 'Flags', 'Calibration Due Date']
    
    def __init__(self):
        self.radiometer = serial.Serial('/dev/ttyUSB0', 2400, timeout=1)
        
        # Send p character to initialize data transfer from radiometer
        self.radiometer.write(b'p')

    def clearRadiometerInternalDataStorage(self):
        # Clear UV readings stored in the Solar Light Radiometer internal storage
        self.radiometer.write(b'\x03')
        sleep(1)
        self.radiometer.write(b'y')
        sleep(1)
        self.radiometer.readline()

    def getReading(self):
        try:
            reading = self.radiometer.readline().decode('iso8859-15').replace('\0', '')
        except:
            return None
        
        if len(reading) == 0:
            return None
        
        try:
            data =list(csv.DictReader(reading.splitlines(), self.columns, dialect='excel'))[0]
        except Exception as e:
            print(e)
            return self.getEmptyReading()

        return data

    def getEmptyReading(self):
        return {key: '' for key in self.columns}

    def stop(self):
        self.radiometer.close()