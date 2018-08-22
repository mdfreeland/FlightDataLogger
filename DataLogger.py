from Readers.RadiometryReader import RadiometryReader
from Readers.AltimeterReader import AltimeterReader
from Readers.LuxSensorReader import LuxSensorReader
from CsvWriter import CsvWriter
from datetime import datetime

class DataLogger:
    def __init__(self, shouldClearRadiometerInternalDataStorage):
        self.radiometerReader = RadiometryReader()
        self.altimeterReader = AltimeterReader()
        self.luxSensorReader = LuxSensorReader()
        self.csvWriter = CsvWriter()

        self.shouldClearRadiometerInternalDataStorage = shouldClearRadiometerInternalDataStorage
        self.lastRadiometerReading = datetime.min

    def start(self):
        if self.shouldClearRadiometerInternalDataStorage:
            self.radiometerReader.clearRadiometerInternalDataStorage()
            return
        
        try:
            while (True):
                uvReading = self.radiometerReader.getReading()
                if uvReading is not None:
                    print(uvReading)
                    altimeterReading = self.altimeterReader.getReading()
                    print(altimeterReading)
                    lightIntensityReading = self.luxSensorReader.getReading()
                    print(lightIntensityReading)
                    self.csvWriter.writeCsvRow(uvReading, altimeterReading, lightIntensityReading)
        except KeyboardInterrupt:
            self.radiometerReader.stop()
            self.csvWriter.closeWriter()
            return