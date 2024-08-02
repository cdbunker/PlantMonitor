import os
import json
from datetime import datetime
from plant_monitor.utils.config import get_config


class DataHandler:
    def __init__(self, config_path):
        self.config = get_config(config_path)
        self.data_file_path = self.config['data_file_path']

        # Ensure the directory for the data file exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)

    def add_sensor_data(self, uuid, temperature, humidity):
        data_entry = {
            'uuid': uuid,
            'temperature': temperature,
            'humidity': humidity,
            'timestamp': datetime.utcnow().isoformat()
        }
        with open(self.data_file_path, 'a') as file:
            file.write(json.dumps(data_entry) + '\n')

    def get_all_data(self):
        data = []
        if os.path.exists(self.data_file_path):
            with open(self.data_file_path, 'r') as file:
                for line in file:
                    data.append(json.loads(line.strip()))
        return data
