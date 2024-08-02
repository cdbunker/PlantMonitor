import socket
import json
from plant_monitor.utils.config import get_config


class ArduinoInterface:
    def __init__(self, config_path):
        self.config = get_config(config_path)
        self.host = self.config['host']
        self.port = self.config['port']
        self.buffer_size = self.config['buffer_size']
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Listening on {self.host}:{self.port}")

    def receive_data(self):
        client_socket, addr = self.server_socket.accept()
        print(f"Connection from {addr}")
        data = client_socket.recv(self.buffer_size)
        client_socket.close()
        return json.loads(data)

    def close(self):
        self.server_socket.close()
