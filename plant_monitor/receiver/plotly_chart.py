from flask import render_template
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta


def plotly_chart(data_processor):
    times, temperatures, humidities = data_processor.load_data()
    try:
        now = datetime.now()
        one_day_ago = now - timedelta(days=1)
        current_temp, current_hum = None, None
        temp_sum, hum_sum = 0, 0
        count = 0

        for i in range(len(times)):
            date_time_isoformat = datetime.fromisoformat(times[i])
            date_time_formatted = date_time_isoformat.strftime('%m/%d %H:%M:%S')
            times[i] = date_time_formatted

            temp = temperatures[i]
            hum = humidities[i]

            if date_time_isoformat >= one_day_ago:
                temp_sum += temp
                hum_sum += hum
                count += 1

        current_temp = temp
        current_hum = hum
        average_temp = temp_sum / count if count != 0 else 0
        average_hum = hum_sum / count if count != 0 else 0

        # Round values
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
        number_of_ticks = data_processor.config.chart_number_ticks
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
