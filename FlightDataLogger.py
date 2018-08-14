#! /usr/bin/env python3

import argparse
from DataLogger import DataLogger

parser = argparse.ArgumentParser()
parser.add_argument("--clear", action="store_true", help="Clear all data stored on Solar Light UV Radiometer internal data logger.")
args = parser.parse_args()

dataLogger = DataLogger(args.clear)
dataLogger.start()