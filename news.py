import requests
import json
import urllib.parse
from datetime import datetime

def get_time_period(current_hour):
    if 5 <= int(current_hour) < 12:
        return "Morning"
    elif 12 <= int(current_hour) < 17:
        return "Afternoon"
    else:
        return "Evening"

def opening_greeting(name, time, date, time_period):
    if time_period == "Morning":
        return f"Good morning, {name}. It's {time} on {date}. We hope you have a great start to your day with our news coverage."
    elif time_period == "Afternoon":
        return f"Good afternoon, {name}. It's {time} on {date}. Welcome to our news broadcast."
    elif time_period == "Evening":
        return f"Good evening, {name}. It's {time} on {date}. Thanks for joining us for the latest news and updates."

class News:
    def __init__(self, name, url_location, address):
        self.name = name
        self.url_location = url_location
        self.address = address
        self.response = requests.get(url_location).json()

    def get_opening_greeting(self):
        current_time = datetime.now()
        date = current_time.strftime("%A, %B %d, %Y")
        time = current_time.strftime("%H %M %p")
        time_period = get_time_period(current_time.strftime("%H"))

        return opening_greeting(self.name, time, date, time_period)

    def get_weather(self, weather_url, weather_api_key):
        latitude = self.response[0]["lat"]
        longitude = self.response[0]["lon"]
        weather_params = {
            "lat": latitude,
            "lon": longitude,
            "appid": weather_api_key,
            "units": "metric"
        }
        weather_response = requests.get(weather_url, params=weather_params)
        weather_data = json.loads(weather_response.text)

        

        rain_volume = weather_data['rain']['1h']
        visibility = weather_data['visibility']
        pressure = weather_data['main']['pressure']
        cloud_cover = weather_data['clouds']['all']
        weather_news = f"""Let's start with the weather. In some parts of the region, we are experiencing {weather_data["weather"][0]["description"]} with a temperature of {weather_data["main"]["temp"]} degrees Celsius. It feels like {weather_data["main"]["feels_like"]} degrees Celsius outside,with a humidity level of {weather_data["main"]["humidity"]} percent. The wind is blowing at a speed of {weather_data["wind"]["speed"]} kilometers per hour coming from {weather_data["wind"]["deg"]} degrees\nThe rain gauge shows approximately {rain_volume} millimeters of rain in the past hour.\nThe visibility is good at {visibility} meters, and the atmospheric pressure is {pressure} hPa.\nCloud cover is at {cloud_cover} percent."""

        return weather_news

    def get_headlines(self, news_api_key, pageSize=5):
        news_url = "https://newsapi.org/v2/top-headlines"
        news_params = {
            "country": "us",
            "pageSize": pageSize,
        }
        news_response = requests.get(news_url, params=news_params, headers={"Authorization": f"Bearer {news_api_key}"})
        news_data = json.loads(news_response.text)
        return news_data["articles"]
address = "Addis Ababa"
name = "John Doe"
url_locations = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
todays_news = News(name, url_locations, address)
"""
print(todays_news.get_opening_greeting())
print(todays_news.get_weather(weather_url="https://api.openweathermap.org/data/2.5/weather", weather_api_key="5e015bee876fa980cbd632e0536d4840"))
print("---"*50)
print(todays_news.get_headlines(news_api_key="c08685d1de5f4a2e894b2161a85cf39d"))
"""