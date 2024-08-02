from plant_monitor.client import Client


def run():
    client_config_path = 'configs/client_config.yaml'
    sensor_config_path = 'configs/sensor_config.yaml'
    client = Client(client_config_path, sensor_config_path)
    client.run()


if __name__ == '__main__':
    run()
