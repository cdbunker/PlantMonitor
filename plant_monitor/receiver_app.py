import os
import yaml
from flask import Flask
from plant_monitor import CONFIGS_PATH
from plant_monitor.receiver.config import Config
from plant_monitor.receiver.plotly_chart import plotly_chart
from plant_monitor.receiver.data_processor import DataProcessor
from plant_monitor.receiver.matplotlib_chart import matplotlib_chart


def create_app(config_path):
    app = Flask(__name__, template_folder='templates')
    config = Config(config_path)
    data_processor = DataProcessor(config)

    app.config.from_object(config)
    setup_routes(app, data_processor)

    return app


def setup_routes(app, data_processor):
    @app.route('/receive_data', methods=['POST'])
    def receive_data():
        return data_processor.receive_data()

    @app.route('/chart')
    def chart():
        return plotly_chart(data_processor)

    @app.route('/chart_matplotlib')
    def chart_matplotlib():
        return matplotlib_chart(data_processor)


def run():
    config_path = os.path.join(CONFIGS_PATH, 'receiver_config.yaml')
    config = Config(config_path)

    data_processor = DataProcessor(config)

    app = Flask(__name__, template_folder='templates')
    setup_routes(app, data_processor)

    app.run(host=config.host, port=config.port, debug=True)


if __name__ == '__main__':
    run()
