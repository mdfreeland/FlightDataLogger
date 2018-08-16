import smbus

# https://github.com/ControlEverythingCommunity/TSL2561

class LuxSensorReader:
    def __init__(self):
        # Get I2C bus
        self.sensor = smbus.SMBus(1)

        # TSL2561 address, 0x39(57)
        # Select control register, 0x00(00) with command register, 0x80(128)
        #		0x03(03)	Power ON mode
        self.sensor.write_byte_data(0x39, 0x00 | 0x80, 0x03)
        # TSL2561 address, 0x39(57)
        # Select timing register, 0x01(01) with command register, 0x80(128)
        #		0x02(02)	Nominal integration time = 402ms
        self.sensor.write_byte_data(0x39, 0x01 | 0x80, 0x02)

    def getReading(self):
        # Read data back from 0x0C(12) with command register, 0x80(128), 2 bytes
        # ch0 LSB, ch0 MSB
        data = self.sensor.read_i2c_block_data(0x39, 0x0C | 0x80, 2)

        # Read data back from 0x0E(14) with command register, 0x80(128), 2 bytes
        # ch1 LSB, ch1 MSB
        data1 = self.sensor.read_i2c_block_data(0x39, 0x0E | 0x80, 2)

        # Convert the data
        ch0 = data[1] * 256 + data[0]
        ch1 = data1[1] * 256 + data1[0]

        return {'Full Spectrum (lux)': '{0:0.3f}'.format(ch0), 'Infrared Light (lux)': '{0:0.3f}'.format(ch1), 'Visible Light (lux)': '{0:0.3f}'.format(ch0 - ch1)}