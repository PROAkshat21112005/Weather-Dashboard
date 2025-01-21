from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
api_key = os.getenv("OPENWEATHER_API_KEY", "3fefe0e8b49a4267c906b1573d5fce18")  

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    error_message = None

    if request.method == 'POST':
        city = request.form.get('city').strip()
        if city:
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": api_key,
                "units": "metric"
            }
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                weather_data = {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temp": data["main"]["temp"],
                    "feel_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "condition": data["weather"][0]["description"].capitalize(),
                    "wind_speed": data["wind"]["speed"],
                    "sunrise": data["sys"]["sunrise"],
                    "sunset": data["sys"]["sunset"],
                    "pressure": data["main"]["pressure"],
                    "visibility": data["visibility"],
                    "icon": data["weather"][0]["icon"]  # Retrieve the icon code
                }
            except requests.exceptions.RequestException:
                error_message = "Unable to fetch weather data. Please check the city name and try again."
        else:
            error_message = "City name cannot be empty. Please enter a valid city."

    return render_template("index2.html", weather=weather_data, error=error_message)

if __name__ == "__main__":
    app.run(debug=True)
