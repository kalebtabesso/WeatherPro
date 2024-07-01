import requests
import pandas as pd

def get_forecast_url(latitude, longitude):
    base_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    response = requests.get(base_url)
    response.raise_for_status()
    data = response.json()
    return data['properties']['forecast']

def get_weather_data(forecast_url):
    response = requests.get(forecast_url)
    response.raise_for_status()
    data = response.json()
    return data['properties']['periods']

def save_weather_data(weather_data, filename):
    with open(filename, 'w') as file:
        for period in weather_data:
            file.write(f"{period['name']},{period['startTime']},{period['temperature']},{period['temperatureUnit']},{period['shortForecast']}\n")

def generate_html(weather_data, html_filename):
    html_content = """
    <html>
    <head>
        <title>Weather Forecast</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-image: url('static/background.jpg');
                background-size: cover;
                background-repeat: no-repeat;
                color: #333;
            }
            .container {
                width: 80%;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.8);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h2 {
                text-align: center;
                color: #4c93af;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            table, th, td {
                border: 1px solid #ddd;
            }
            th, td {
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #4c9baf;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Weather Forecast</h2>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Start Time</th>
                    <th>Temperature</th>
                    <th>Forecast</th>
                </tr>
    """

    for period in weather_data:
        html_content += f"""
                <tr>
                    <td>{period['name']}</td>
                    <td>{period['startTime']}</td>
                    <td>{period['temperature']} {period['temperatureUnit']}</td>
                    <td>{period['shortForecast']}</td>
                </tr>
        """

    html_content += """
            </table>
        </div>
    </body>
    </html>
    """

    with open(html_filename, 'w') as file:
        file.write(html_content)

def main():
    try:
        latitude = input("Enter the latitude: ")
        longitude = input("Enter the longitude: ")

        forecast_url = get_forecast_url(latitude, longitude)
        weather_data = get_weather_data(forecast_url)
        
        text_filename = "weather_data.txt"
        save_weather_data(weather_data, text_filename)
        print(f"Weather data saved to {text_filename}")
        
        html_filename = "weather_forecast.html"
        generate_html(weather_data, html_filename)
        print(f"Weather forecast HTML generated: {html_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except KeyError as e:
        print(f"Error parsing data: Missing key {e}")

if __name__ == "__main__":
    main()
