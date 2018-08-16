from Readers.RadiometryReader import RadiometryReader
from Readers.AltimeterReader import AltimeterReader
from Readers.LuxSensorReader import LuxSensorReader
from datetime import datetime

class DataLogger:
    def __init__(self, clearRadiometerInternalDataStorage):
        self.radiometerReader = RadiometryReader(clearRadiometerInternalDataStorage)
        self.altimeterReader = AltimeterReader()
        self.LuxSensorReader = LuxSensorReader()
        self.lastRadiometerReading = datetime.min

    def start(self):
        try:
            while (True):
                uvReading = self.radiometerReader.getReading()
                if uvReading is not None:
                    print(uvReading)
                    altimeterReading = self.altimeterReader.getReading()
                    print(altimeterReading)
                    lightIntensityReading = self.LuxSensorReader.getReading()
                    print(lightIntensityReading)
        finally:
            self.radiometerReader.stop()