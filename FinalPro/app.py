from flask import Flask, render_template, request
import requests

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
  
    if request.method == 'POST':
        try:
            latitude = request.form['latitude']
            longitude = request.form['longitude']

            forecast_url = get_forecast_url(latitude, longitude)
            weather_data = get_weather_data(forecast_url)
        except requests.exceptions.RequestException as e:
            error = f"Error fetching data: {e}"
        except KeyError as e:
            error = f"Error parsing data: Missing key {e}"

    return render_template('index.html', weather_data=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
