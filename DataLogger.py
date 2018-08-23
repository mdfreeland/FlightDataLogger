from Readers.RadiometryReader import RadiometryReader
from Readers.AltimeterReader import AltimeterReader
from Readers.LuxSensorReader import LuxSensorReader
from Readers.GpsReader import GpsReader
from CsvWriter import CsvWriter
from datetime import datetime
from datetime import timedelta
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
        self.gpsReader = GpsReader()
        self.gpsReader.start()
        self.csvWriter = CsvWriter()

        self.shouldClearRadiometerInternalDataStorage = shouldClearRadiometerInternalDataStorage
        self.lastRadiometerReading = datetime.min

    def start(self):
        if self.shouldClearRadiometerInternalDataStorage:
            self.radiometerReader.clearRadiometerInternalDataStorage()
            self.radiometerReader.stop()
            self.gpsReader.running = False
            return
        
        try:
            while (True):
                uvReading = self.radiometerReader.getReading()
                if uvReading is not None or self.lastRadiometerReading + timedelta(seconds=10) <= datetime.now():
                    print(uvReading)
                    altimeterReading = self.altimeterReader.getReading()
                    print(altimeterReading)
                    lightIntensityReading = self.luxSensorReader.getReading()
                    print(lightIntensityReading)
                    gpsReading = self.gpsReader.getReading()
                    print(gpsReading)
                    self.csvWriter.writeCsvRow(uvReading or self.radiometerReader.getEmptyReading(), altimeterReading, lightIntensityReading, gpsReading)
                    self.lastRadiometerReading = datetime.now()
        except (KeyboardInterrupt, SystemExit):
            self.gpsReader.running = False
            message = 'SIGINT Received. Shutting down...'
            self.logger.info(message)
            print(message)
        except Exception:
            self.logger.exception('FlightDataLogger Terminating:')
        finally:
            self.radiometerReader.stop()
            self.csvWriter.closeWriter()

