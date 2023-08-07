# Text to speech

import pyttsx3
from news import News
import urllib.parse

class ReadNews:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.engine.setProperty("volume", 1.0)
        self.address = "Addis Ababa"
        self.name = "John Doe"
        self.url_locations = url_locations = f'https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(self.address)}&format=json'
        self.news_instance = News(self.name, self.url_locations, self.address)
    
    def read_loud(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def read_opening_greeting(self):
        opening_greeting_text = self.news_instance.get_opening_greeting()
        self.read_loud(opening_greeting_text)

    def read_weather(self):
        weather_text = self.news_instance.get_weather(weather_url="https://api.openweathermap.org/data/2.5/weather", weather_api_key="5e015bee876fa980cbd632e0536d4840")
        self.read_loud(weather_text)

    def read_headlines(self):
        self.read_loud("Let's, move on to the headlines of the day.")
        for article in self.news_instance.get_headlines(news_api_key="c08685d1de5f4a2e894b2161a85cf39d"):
            title = article["title"]
            description = article["description"]
            source = article["source"]["name"]

            text = f"{title}. {description}."

            self.read_loud(text)
    

    
