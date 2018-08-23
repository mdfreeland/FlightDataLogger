from Readers.RadiometryReader import RadiometryReader
from Readers.AltimeterReader import AltimeterReader
from Readers.LuxSensorReader import LuxSensorReader
from CsvWriter import CsvWriter
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

class DataLogger:
    def __init__(self, shouldClearRadiometerInternalDataStorage):
        self.logger = logging.getLogger('FlightDataLogger')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = RotatingFileHandler('FlightDataLogger.log', maxBytes=2000000, backupCount=10)
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)
        
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
        except Exception:
            self.logger.exception('FlightDataLogger Terminating:')
        finally:
            self.radiometerReader.stop()
            self.csvWriter.closeWriter()