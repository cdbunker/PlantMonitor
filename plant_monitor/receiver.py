import os
import time
from plant_monitor.arduino.arduino_interface import ArduinoInterface
from plant_monitor.database.data_handler import DataHandler
from plant_monitor.flask_app.routes import create_app


def main():
    config_path = os.path.join(os.path.dirname(__file__), 'configs')
    arduino_interface = ArduinoInterface(os.path.join(config_path, 'arduino_config.yaml'))
    data_handler = DataHandler(os.path.join(config_path, 'database_config.yaml'))

    app = create_app(os.path.join(config_path, 'flask_config.yaml'))

    def aggregate_data():
        while True:
            try:
                data = arduino_interface.receive_data()
                data_handler.add_sensor_data(data['uuid'], data['temperature'], data['humidity'])
            except Exception as e:
                print(f"Error receiving data: {e}")
            time.sleep(1)  # Adjust the sleep time as needed

    from threading import Thread
    data_thread = Thread(target=aggregate_data)
    data_thread.start()

    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
