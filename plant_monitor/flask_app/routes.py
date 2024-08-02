import json
import plotly
import plotly.graph_objs as go
from flask import Flask, render_template, jsonify
from plant_monitor.database.data_handler import DataHandler


def create_app(config_path):
    app = Flask(__name__)
    app.config.from_file(config_path, load=lambda x: json.load(open(x)))
    data_handler = DataHandler(app.config['DATA_FILE_PATH'])

    @app.route('/')
    def index():
        data = data_handler.get_all_data()
        times = [d.timestamp for d in data]
        temperatures = [d.temperature for d in data]
        humidities = [d.humidity for d in data]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=times, y=temperatures, mode='lines+markers', name='Temperature'))
        fig.add_trace(go.Scatter(x=times, y=humidities, mode='lines+markers', name='Humidity'))

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('chart.html', graphJSON=graphJSON)

    @app.route('/data')
    def data():
        data = data_handler.get_all_data()
        result = [{'uuid': d.uuid, 'temperature': d.temperature, 'humidity': d.humidity, 'timestamp': d.timestamp} for d in data]
        return jsonify(result)

    return app
