import requests
import json
import math

base_url = "http://api.openweathermap.org/data/2.5/weather?q="

class WeatherApiClient():
    def __init__(self, api_key, city, language="en"):
        self.key = api_key
        self.city = city
        self.language = language

    def _api_call(self):
        request = requests.get(base_url + self.city + "&appid=" + self.key + "&units=metric" + "&lang=" + self.language)
        data = json.loads(request.content)
        return data

    def get_temperature(self):
        data = self._api_call()

        return math.ceil(int(data["main"]["temp"]))
    
    def get_weather(self):
        data = self._api_call()

        return data["weather"][0]["description"]