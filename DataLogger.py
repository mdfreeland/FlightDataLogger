from Readers.RadiometryReader import RadiometryReader
from Readers.AltimeterReader import AltimeterReader
from datetime import datetime

class DataLogger:
    def __init__(self, clearRadiometerInternalDataStorage):
        self.radiometerReader = RadiometryReader(clearRadiometerInternalDataStorage)
        self.altimeterReader = AltimeterReader()
        self.lastRadiometerReading = datetime.min

    def start(self):
        try:
            while (True):
                uvReading = self.radiometerReader.getReading()
                if uvReading is not None:
                    print(uvReading)
                    altimeterReading = self.altimeterReader.getReading()
                    print(altimeterReading)
        finally:
            self.radiometerReader.stop()