import requests


class Sender:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port

    def send_data(self, data):
        url = f'http://{self.server_ip}:{self.server_port}/receive_data'
        try:
            response = requests.post(url, json=data)
            print(f'Status Code: {response.status_code}, Response: {response.text}')
            return True
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            return False
