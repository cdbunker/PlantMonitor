from .base_humidity_sensor import BaseHumiditySensor
from .base_temperature_sensor import BaseTemperatureSensor
import time
import yaml
import smbus2


class SHT30Sensor(BaseHumiditySensor, BaseTemperatureSensor):
    def __init__(self, config_path):
        super().__init__()
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.bus = smbus2.SMBus(1)
        self.address = config['i2c_address']

    def read_temperature(self):
        self.bus.write_byte(self.address, 0x2C)
        time.sleep(0.5)
        data = self.bus.read_i2c_block_data(self.address, 0x00, 6)
        temp = data[0] << 8 | data[1]
        temp = -45 + (175 * temp / 65535.0)
        return temp

    def read_humidity(self):
        self.bus.write_byte(self.address, 0x2C)
        time.sleep(0.5)
        data = self.bus.read_i2c_block_data(self.address, 0x00, 6)
        humidity = data[3] << 8 | data[4]
        humidity = 100 * (humidity / 65535.0)
        return humidity

    def read(self):
        temperature = self.read_temperature()
        humidity = self.read_humidity()
        return {'temperature': temperature, 'humidity': humidity}
