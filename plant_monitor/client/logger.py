import os
import json


class Logger:
    def __init__(self, local_log_path):
        self.local_log_path = local_log_path

    def log_data_locally(self, data):
        with open(self.local_log_path, 'a') as file:
            file.write(json.dumps(data) + '\n')
