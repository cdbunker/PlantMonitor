from .base_humidity_sensor import BaseHumiditySensor
from .base_temperature_sensor import BaseTemperatureSensor
from plant_monitor.utilities import celcius_to_fahrenheit
import yaml
import board
import adafruit_dht


class DHT22Sensor(BaseHumiditySensor, BaseTemperatureSensor):
    def __init__(self, config_path):
        super().__init__()
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
        except RuntimeError as e:
            print(f"Error reading DHT22 sensor: {e}")
            return {'temperature': None, 'humidity': None}
