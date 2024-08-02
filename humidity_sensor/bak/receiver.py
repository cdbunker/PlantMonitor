import os
from flask import Flask, request, render_template
import yaml
import json
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime, timedelta


class Receiver:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.host = self.config['host']
        self.port = self.config['port']
        self.data_log_path = self.config.get('data_log_path')

        if not os.path.exists(os.path.dirname(self.data_log_path)):
            os.makedirs(os.path.dirname(self.data_log_path))
        if not os.path.exists(self.data_log_path):
            with open(self.data_log_path, 'w') as f:
                f.write('')

        self.app = Flask(__name__, template_folder='templates')
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/receive_data', methods=['POST'])
        def receive_data():
            data = request.get_json()
            if data:
                with open(self.data_log_path, 'a') as f:
                    f.write(json.dumps(data) + '\n')
                print(f"Received data: Time: {data['time']}, Temperature: {data['temperature']} C, Humidity: {data['humidity']}%")
                return "Data received", 200
            else:
                return "No data received", 400

        @self.app.route('/chart_matplotlib')
        def chart_matplotlib():
            times, temperatures, humidities = [], [], []
            try:
                with open(self.data_log_path, 'r') as f:
                    for line in f:
                        entry = json.loads(line)
                        date_time_isoformat = datetime.fromisoformat(entry.get('time'))
                        month = date_time_isoformat.month
                        day = date_time_isoformat.day
                        hour = date_time_isoformat.hour
                        minute = date_time_isoformat.minute
                        second = date_time_isoformat.second
                        date_time_formatted = f'{month}/{day} {hour}:{minute}:{second}'
                        times.append(date_time_formatted)
                        temperatures.append(entry.get('temperature'))
                        humidities.append(entry.get('humidity'))

                fig, ax1 = plt.subplots()

                ax1.set_xlabel('Time')
                ax1.set_ylabel('Temperature (C)', color='tab:red')
                ax1.plot(times, temperatures, 'r-')
                ax1.tick_params(axis='y', labelcolor='tab:red')

                # Set y-axis limits for temperature
                temp_min, temp_max = min(temperatures), max(temperatures)
                ax1.set_ylim(temp_min - self.config['chart_padding'], temp_max + self.config['chart_padding'])

                ax2 = ax1.twinx()
                ax2.set_ylabel('Humidity (%)', color='tab:blue')
                ax2.plot(times, humidities, 'b-')
                ax2.tick_params(axis='y', labelcolor='tab:blue')

                # Set y-axis limits for humidity
                hum_min, hum_max = min(humidities), max(humidities)
                ax2.set_ylim(hum_min - self.config['chart_padding'], hum_max + self.config['chart_padding'])

                # Format x-axis
                # only show 100 ticks on x-axis unless there are less than 100 data points
                if len(times) > self.config['chart_number_ticks']:
                    ax1.set_xticks(times[::len(times) // self.config['chart_number_ticks']])
                else:
                    ax1.set_xticks(times)

                fig.autofmt_xdate(rotation=90)  # Rotate x-axis text

                fig.tight_layout()

                img = BytesIO()
                plt.savefig(img, format='png')
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode()

                return render_template('matplotlib_chart.html', plot_url=plot_url)
            except Exception as e:
                print(f"Error generating chart: {e}")
                return "Error generating chart", 500

        @self.app.route('/chart')
        def chart():
            times, temperatures, humidities = [], [], []
            try:
                now = datetime.now()
                one_day_ago = now - timedelta(days=1)
                current_temp, current_hum = None, None
                temp_sum, hum_sum = 0, 0
                count = 0

                with open(self.data_log_path, 'r') as f:
                    for line in f:
                        entry = json.loads(line)
                        date_time_isoformat = datetime.fromisoformat(entry.get('time'))
                        date_time_formatted = date_time_isoformat.strftime('%m/%d %H:%M:%S')
                        times.append(date_time_formatted)
                        temp = entry.get('temperature')
                        hum = entry.get('humidity')
                        temperatures.append(temp)
                        humidities.append(hum)

                        if date_time_isoformat >= one_day_ago:
                            temp_sum += temp
                            hum_sum += hum
                            count += 1

                current_temp = temp
                current_hum = hum
                average_temp = temp_sum / count if count != 0 else 0
                average_hum = hum_sum / count if count != 0 else 0

                # Take each to the nearest 2 decimal places
                current_temp = round(current_temp, 2) if current_temp is not None else None
                current_hum = round(current_hum, 2) if current_hum is not None else None
                average_temp = round(average_temp, 2)
                average_hum = round(average_hum, 2)

                fig = make_subplots(specs=[[{"secondary_y": True}]])

                # Add traces
                fig.add_trace(
                    go.Scatter(x=times, y=temperatures, name="Temperature (C)", mode='lines+markers',
                               line=dict(color='red')),
                    secondary_y=False,
                )

                fig.add_trace(
                    go.Scatter(x=times, y=humidities, name="Humidity (%)", mode='lines+markers',
                               line=dict(color='blue')),
                    secondary_y=True,
                )

                # Set y-axis titles
                fig.update_yaxes(title_text="Temperature (C)", secondary_y=False)
                fig.update_yaxes(title_text="Humidity (%)", secondary_y=True)

                # Format x-axis
                number_of_ticks = self.config.get('chart_number_ticks', 100)
                fig.update_xaxes(title_text="Time", tickangle=90, tickmode='array',
                                 tickvals=times[::len(times) // number_of_ticks])

                # Update layout
                fig.update_layout(
                    title_text="Sensor Data",
                    font=dict(size=14),
                    autosize=True,
                    height=600,
                    margin=dict(l=40, r=40, t=40, b=40)
                )

                chart_html = fig.to_html(full_html=False)

                return render_template(
                    'plotly_chart.html',
                    chart_html=chart_html,
                    current_temp=current_temp,
                    current_hum=current_hum,
                    average_temp=average_temp,
                    average_hum=average_hum
                )
            except Exception as e:
                print(f"Error generating chart: {e}")
                return "Error generating chart", 500

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=True)


if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), 'configs/receiver_config.yaml')
    receiver = Receiver(config_path)
    receiver.run()
