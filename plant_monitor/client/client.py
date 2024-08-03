import time
from datetime import datetime
from .config import Config
from .logger import Logger
from .sender import Sender
from plant_monitor.sensor import DHT22Sensor, SHT30Sensor


class Client:
    def __init__(self, client_config_path, sensor_config_path):
        self.config = Config(client_config_path)
        self.sensor = DHT22Sensor(sensor_config_path)
        self.logger = Logger(self.config.local_log_path)
        self.sender = Sender(self.config.server_ip, self.config.server_port)

    def run(self):
        while True:
            data = self.sensor.read()
            data['time'] = datetime.now().isoformat()
            if data['temperature'] is not None and data['humidity'] is not None:
                if not self.sender.send_data(data):
                    print(f'Could not send data. Logging data locally: {data}')
                    self.logger.log_data_locally(data)
            time.sleep(self.config.log_delay)
