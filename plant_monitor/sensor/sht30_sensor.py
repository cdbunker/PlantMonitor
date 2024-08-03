from plant_monitor.sensor.base_humidity_sensor import BaseHumiditySensor
from plant_monitor.sensor.base_temperature_sensor import BaseTemperatureSensor
import time
import yaml
import smbus2


class SHT30Sensor(BaseHumiditySensor, BaseTemperatureSensor):
    def __init__(self, config_path):
        super().__init__()
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.bus = smbus2.SMBus(1)
        self.address = config['i2c_address']  # 0x44(68)

    def read(self):
        # Send measurement command, 0x2C(44); 0x06(06)	High repeatability measurement
        self.bus.write_i2c_block_data(self.address, 0x2C, [0x06])
        time.sleep(0.5)

        # Read data back from 0x00(00), 6 bytes
        # cTemp MSB, cTemp LSB, cTemp CRC, Humididty MSB, Humidity LSB, Humidity CRC
        data = self.bus.read_i2c_block_data(self.address, 0x00, 6)
        temperature = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45

        humidity = data[3] << 8 | data[4]
        humidity = 100 * (humidity / 65535.0)

        return {'temperature': temperature, 'humidity': humidity}



if __name__ == '__main__':
    sensor = SHT30Sensor('configs/sensor_config.yaml')
    print(sensor.read())
