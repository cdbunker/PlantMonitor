from client import Client


if __name__ == '__main__':
    client_config_path = 'configs/client_config.yaml'
    sensor_config_path = 'configs/sensor_config.yaml'
    client = Client(client_config_path, sensor_config_path)
    client.run()
