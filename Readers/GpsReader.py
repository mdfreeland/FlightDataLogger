import threading
import time
import logging
from gps import *

class GpsReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger('FlightDataLogger.GpsReader')
        self.logger.info('GPS Reader initializing...')
        self.session = gps("localhost", "2947", mode=WATCH_ENABLE)
        self.currentValue = None
        self.running = True

    def getReading(self):
        keys = ['epx', 'mode', 'device', 'epv', 'lon', 'climb', 'track', 'alt', 'epc', 'eps', 'time', 'ept', 'speed', 'lat', 'class', 'epy']
        currentValue = self.currentValue
        if currentValue == None:
            return {key: '' for key in keys}
        self.logger.info('GPS reading received: ' + str(currentValue))
        reading = {k:currentValue[k] for k in keys}
        return reading

    def run(self):
        try:
            while self.running:
                val = self.session.next()
                if val['class'] == 'TPV':
                    self.currentValue = val
        except (KeyboardInterrupt, SystemExit):
            raise
        except KeyError:
            pass
        except StopIteration:
            self.session = None
            print("GPSD has terminated")