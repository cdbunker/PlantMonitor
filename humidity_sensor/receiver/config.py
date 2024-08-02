import os
import yaml


class Config:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.host = config['host']
        self.port = config['port']
        self.data_log_path = config.get('data_log_path')
        self.chart_padding = config.get('chart_padding', 5)
        self.chart_number_ticks = config.get('chart_number_ticks', 100)

        if not os.path.exists(os.path.dirname(self.data_log_path)):
            os.makedirs(os.path.dirname(self.data_log_path))
        if not os.path.exists(self.data_log_path):
            with open(self.data_log_path, 'w') as f:
                f.write('')
