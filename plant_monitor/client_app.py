import os
from plant_monitor import CONFIGS_PATH
from plant_monitor.client import Client


def run():
    client_config_path = os.path.join(CONFIGS_PATH, 'configs/client_config.yaml')
    sensor_config_path = os.path.join(CONFIGS_PATH, 'configs/sensor_config.yaml')
    client = Client(client_config_path, sensor_config_path)
    client.run()


if __name__ == '__main__':
    run()
