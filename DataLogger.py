from RadiometryReader import RadiometryReader

class DataLogger:
    def __init__(self, clearRadiometerInternalDataStorage):
        self.radiometerReader = RadiometryReader(clearRadiometerInternalDataStorage)

    def start(self):
        try:
            while (True):
                uvReading = self.radiometerReader.getReading()
                if uvReading is not None:
                    print(uvReading)
        finally:
            self.radiometerReader.stop()