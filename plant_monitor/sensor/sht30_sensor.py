from plant_monitor.sensor.base_humidity_sensor import BaseHumiditySensor
from plant_monitor.sensor.base_temperature_sensor import BaseTemperatureSensor
import time
import yaml
import smbus2


class SHT30Sensor(BaseHumiditySensor, BaseTemperatureSensor):
    CLEAR_STATUS_CMD = b'\x30\x41'
    RESET_CMD = b'\x30\xA2'
    STATUS_CMD = b'\xF3\x2D'
    POLYNOMIAL = 0x131  # P(x) = x^8 + x^5 + x^4 + 1 = 100110001

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

    def send_cmd(self, cmd_request, response_size=6, read_delay_ms=100):
        """
        Send a command to the sensor and read (optionally) the response.
        The responded data is validated by CRC.
        """
        try:
            self.bus.write_i2c_block_data(self.address, cmd_request[0], cmd_request[1:])
            if not response_size:
                return
            time.sleep(read_delay_ms / 1000.0)
            data = self.bus.read_i2c_block_data(self.address, 0x00, response_size)
            for i in range(response_size // 3):
                if not self._check_crc(data[i * 3:(i + 1) * 3]):  # pos 2 and 5 are CRC
                    raise ValueError("CRC Error")
            if data == bytearray(response_size):
                raise ValueError("Data Error")
            return data
        except OSError as ex:
            if 'I2C' in ex.args[0]:
                raise ValueError("Bus Error")
            raise ex

    def _check_crc(self, data):
        # calculates 8-Bit checksum with given polynomial
        crc = 0xFF

        for b in data[:-1]:
            crc ^= b;
            for _ in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ SHT30.POLYNOMIAL;
                else:
                    crc <<= 1
        crc_to_check = data[-1]
        return crc_to_check == crc

    def clear_status(self):
        """
        Clear the status register.
        """
        return self.send_cmd(self.CLEAR_STATUS_CMD, None)

    def reset(self):
        """
        Send a soft-reset to the sensor.
        """
        return self.send_cmd(self.RESET_CMD, None)

    def status(self, raw=False):
        """
        Get the sensor status register.
        It returns an int value or the bytearray(3) if raw == True.
        """
        data = self.send_cmd(self.STATUS_CMD, 3, read_delay_ms=20)

        if raw:
            return data

        status_register = data[0] << 8 | data[1]
        return status_register


if __name__ == '__main__':
    sensor = SHT30Sensor('configs/sensor_config.yaml')
    print(sensor.read())
