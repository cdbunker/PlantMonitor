from flask import render_template
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def matplotlib_chart(data_processor):
    times, temperatures, humidities = data_processor.load_data()
    try:
        fig, ax1 = plt.subplots()

        ax1.set_xlabel('Time')
        ax1.set_ylabel('Temperature (C)', color='tab:red')
        ax1.plot(times, temperatures, 'r-')
        ax1.tick_params(axis='y', labelcolor='tab:red')

        # Set y-axis limits for temperature
        temp_min, temp_max = min(temperatures), max(temperatures)
        ax1.set_ylim(temp_min - data_processor.config.chart_padding, temp_max + data_processor.config.chart_padding)

        ax2 = ax1.twinx()
        ax2.set_ylabel('Humidity (%)', color='tab:blue')
        ax2.plot(times, humidities, 'b-')
        ax2.tick_params(axis='y', labelcolor='tab:blue')

        # Set y-axis limits for humidity
        hum_min, hum_max = min(humidities), max(humidities)
        ax2.set_ylim(hum_min - data_processor.config.chart_padding, hum_max + data_processor.config.chart_padding)

        # Format x-axis
        # only show 100 ticks on x-axis unless there are less than 100 data points
        if len(times) > data_processor.config.chart_number_ticks:
            ax1.set_xticks(times[::len(times) // data_processor.config.chart_number_ticks])
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
