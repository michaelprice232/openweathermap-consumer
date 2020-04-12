# openweathermap-consumer

Script to query the weather from the OpenWeatherMap open data project: https://openweathermap.org/api

Uses a wrapper library: https://pypi.org/project/pyowm/

Requires the `OPEN_WEATHER_MAP_API_KEY` key to be set in the `.env` file, equal to your OWM API key (free to create via the above link). e.g. 
```
OPEN_WEATHER_MAP_API_KEY=<api-key>
```

Gets the weather report from the OWM API (sampled in 3 hour increments for the free tier) for up to 5 days in the future.

## Getting Started
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python weather_api.py
```

## Example Output

```
% python weather_api.py

How many days are there (0-5) before you arrive? 0
Which city or town are you visiting in UK? Manchester
We are finding the CURRENT weather...

Weather forecast for: 2020-04-12 15:24:46 at Manchester, UK
Overall Outlook: few clouds
Clouds: 20 percent chance of rain
Temperature: 18.09 degrees Celsius
Wind: 1 meter/sec
Rain: 0 meters cubed over 3 hours
```