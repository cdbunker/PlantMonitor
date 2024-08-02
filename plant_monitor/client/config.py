import yaml
import os


class Config:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.server_ip = config['server_ip']
        self.server_port = config['server_port']
        self.local_log_path = config.get('local_log_path')
        self.log_delay = config.get('log_delay')  # Default to 60 seconds if not specified

        if not os.path.exists(os.path.dirname(self.local_log_path)):
            os.makedirs(os.path.dirname(self.local_log_path))
        if not os.path.exists(self.local_log_path):
            with open(self.local_log_path, 'w') as f:
                f.write('')
