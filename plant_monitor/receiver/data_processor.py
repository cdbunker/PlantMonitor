import json
from flask import request


class DataProcessor:
    def __init__(self, config):
        self.config = config

    def receive_data(self):
        data = request.get_json()
        if data is not None and data['temperature'] is not None and data['humidity'] is not None:
            with open(self.config.data_log_path, 'a') as f:
                f.write(json.dumps(data) + '\n')
            print(f"Received data: Time: {data['time']}, Temperature: {data['temperature']} C, Humidity: {data['humidity']}%")
            return "Data received", 200
        else:
            return "No data received", 400

    def load_data(self):
        times, temperatures, humidities = [], [], []
        try:
            with open(self.config.data_log_path, 'r') as f:
                for line in f:
                    entry = json.loads(line)
                    times.append(entry['time'])
                    temperatures.append(entry['temperature'])
                    humidities.append(entry['humidity'])
            return times, temperatures, humidities
        except Exception as e:
            print(f"Error loading data: {e}")
            return times, temperatures, humidities
