import serial

class RadiometryReader:
    def __init__(self, clearRadiometerInternalDataStorage):
        self.radiometer = serial.Serial('/dev/ttyUSB0', 2400, timeout=1)
        
        # Clear UV readings stored in the Solar Light Radiometer internal storage
        if clearRadiometerInternalDataStorage:
            self.radiometer.write(b'\x03')
            self.radiometer.write(b'y')

        # Send p character to initialize data transfer from radiometer
        self.radiometer.write(b'p')

    def getReading(self):
        reading = self.radiometer.readline()
        return reading if len(reading) > 0 else None

    def stop(self):
        self.radiometer.close()