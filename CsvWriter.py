import csv
import datetime

class CsvWriter:
    def __init__(self):
        fileName = 'FlightDataLog-' + datetime.datetime.now().strftime('%y%m%d%H%M%S%f') + '.csv'
        self.outputFileWriter = open(fileName, 'w')
        self.csvWriter = csv.DictWriter(self.outputFileWriter, ['Time Reading Written', 'Detector Type', 'Serial Number', 'Record Date', 'Record Time', 'Recorded Value', 'Units', 'Extra Unit Digits', 'Flags', 'Calibration Due Date', 'Temperature (C)', 'Pressure (hPa)', 'Full Spectrum (lux)', 'Infrared Light (lux)', 'Visible Light (lux)', 'epx', 'mode', 'device', 'epv', 'lon', 'climb', 'track', 'alt', 'epc', 'eps', 'time', 'ept', 'speed', 'lat', 'class', 'epy'], dialect='excel')
        self.csvWriter.writeheader()

    def writeCsvRow(self, radiometryReading, altimeterReading, luxSensorReading, gpsReading):
        row = {**radiometryReading, **altimeterReading, **luxSensorReading, **gpsReading}
        row['Time Reading Written'] = datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S.%f %z')
        #print(row)
        self.csvWriter.writerow(row)
        self.outputFileWriter.flush()

    def closeWriter(self):
        self.outputFileWriter.close()