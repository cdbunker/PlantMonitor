import os
import adafruit_dht
import board
import yaml


def celcius_to_fahrenheit(temperature_in_celcius):
    return temperature_in_celcius * 9.0 / 5.0 + 32


class Sensor:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.pin_number = config['dht_pin']
        self.pin = getattr(board, str(self.pin_number))
        self.sensor = adafruit_dht.DHT22(self.pin)

    def read(self):
        try:
            humidity = self.sensor.humidity
            temperature_celcius = self.sensor.temperature
            temperature_fahrenheit = celcius_to_fahrenheit(temperature_celcius)
            return {'temperature': temperature_fahrenheit, 'humidity': humidity}
        except RuntimeError as error:
            print(f"Sensor reading error: {error}")
            return {'temperature': None, 'humidity': None}


if __name__ == '__main__':
    sensor_config_path = os.path.join(os.path.dirname(__file__), 'configs/sensor_config.yaml')
    print(f"Using sensor config path: {sensor_config_path}")
    sensor = Sensor(config_path=sensor_config_path)
    print(sensor.read())
