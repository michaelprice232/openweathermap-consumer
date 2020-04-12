"""
Script to query the weather from the OpenWeatherMap open data project: https://openweathermap.org/api
Uses a wrapper library: https://pypi.org/project/pyowm/

Requires the 'OPEN_WEATHER_MAP_API_KEY' key to be set in the .env file, equal to your OWM API key (free to create)
"""

import pyowm
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load project config & secrets
load_dotenv()

owm = pyowm.OWM(os.getenv("OPEN_WEATHER_MAP_API_KEY"))      # assign the API key
country = 'UK'          # which country to search in
location = None
forecast_date = None
observation = None
arrive = None

# Retrieve arrival time
while arrive not in range(6):   # permits 0 - 5 days
    try:
        arrive = int(input("How many days are there (0-5) before you arrive? "))
    except ValueError:
        print("Error: You must specify between 0-5 (digits)")

# Determine weather we are evaluating the current or future weather
if arrive == 0:
    current_weather = True
    date_api_limit = False
elif arrive == 5:
    # At the API limit (free tier) of 5 days
    current_weather = False
    date_api_limit = True       # Flag to apply minor modification to date to workaround API limit
else:
    current_weather = False
    date_api_limit = False

# Retrieve location
valid_location = False
while not valid_location:
    try:
        location = input("Which city or town are you visiting in {}? ".format(country))

        if current_weather:
            # Get current weather
            observation = owm.weather_at_place(location + ',' + country)
        else:
            # Get weather forecast (in the future)
            observation = owm.three_hours_forecast(location + ',' + country)       # API permits up to 5 days in future

        # Exit loop as valid location has been found
        valid_location = True
    except:
        print("Invalid city or town name {} in {}. Please enter again.".format(location, country))

# Retrieve weather forecast
if current_weather:
    # Get current weather
    forecast_date = datetime.now()
    print("We are finding the CURRENT weather...")
    weather = observation.get_weather()

else:
    # Get forecast (in the future)
    if date_api_limit:
        print("We are at the API limit of 5 days, so attempting to workaround by dropping the hours slightly")
        forecast_date = datetime.now() + timedelta(days=arrive, hours=-6)       # drop 6 hours, 5 days from now
    else:
        forecast_date = datetime.now() + timedelta(days=arrive)

    print("We are looking at weather in the FUTURE")
    weather = observation.get_weather_at(forecast_date)


# Retrieve weather specifics
description = weather.get_detailed_status()
clouds = weather.get_clouds()                                       # % of cloud coverage
temperature = weather.get_temperature(unit='celsius')['temp']
wind = weather.get_wind()['speed']

# returns an empty dict when there is no rain, so check for KeyError
try:
    rain = weather.get_rain()['all']
except KeyError:
    rain = 0


# Outputs
print("\nWeather forecast for: {} at {}, {}".format(forecast_date.replace(microsecond=0), location, country))
print("Overall Outlook:", description)
print("Clouds:", clouds, "percent chance of rain")
print("Temperature:", temperature, "degrees Celsius")
print("Wind:", wind, "meter/sec")
print("Rain:", rain, "meters cubed over 3 hours")
