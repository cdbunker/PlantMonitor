import os
import requests
import time
import yaml
from sensor import Sensor
import json
from datetime import datetime


class Client:
    def __init__(self, client_config_path, sensor_config_path):
        with open(client_config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.server_ip = self.config['server_ip']
        self.server_port = self.config['server_port']
        self.sensor = Sensor(sensor_config_path)
        self.local_log_path = self.config.get('local_log_path')

        if not os.path.exists(os.path.dirname(self.local_log_path)):
            os.makedirs(os.path.dirname(self.local_log_path))
        if not os.path.exists(self.local_log_path):
            with open(self.local_log_path, 'w') as f:
                f.write('')

    def send_data(self, data):
        url = f'http://{self.server_ip}:{self.server_port}/receive_data'
        try:
            response = requests.post(url, json=data)
            print(f'Status Code: {response.status_code}, Response: {response.text}')
            return True
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            return False

    def log_data_locally(self, data):
        with open(self.local_log_path, 'a') as file:
            file.write(json.dumps(data) + '\n')

    def run(self):
        while True:
            data = self.sensor.read()
            data['time'] = datetime.now().isoformat()
            if data['temperature'] is not None and data['humidity'] is not None:
                if not self.send_data(data):
                    print(f'Could not send data. Logging data locally: {data}')
                    print(f'Logging to {self.local_log_path}')
                    self.log_data_locally(data)
            time.sleep(self.config['log_delay'])


if __name__ == '__main__':
    client_config_path = os.path.join(os.path.dirname(__file__), 'configs/client_config.yaml')
    sensor_config_path = os.path.join(os.path.dirname(__file__), 'configs/sensor_config.yaml')
    client = Client(client_config_path, sensor_config_path)
    client.run()
