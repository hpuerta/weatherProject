import os
import requests
from datetime import datetime

class Weather():
    __city = ""
    __country = ""
    query=""
    __API_URL_WEATHER = ""
    requestWeatherJson={}

    def __init__(self,city:str,country:str)->None:
        self.__city = city
        self.__country = country
        self.query = city + "," + country
        self.__API_URL_WEATHER = f"http://api.openweathermap.org/data/2.5/weather?q={self.query}&units=metric&appid=" + os.getenv("API_KEY")
    
    def getWeatherJson(self):
        self.requestWeatherJson = requests.get(f"{self.__API_URL_WEATHER}").json()

    def getResponseData(self):
        self.getWeatherJson()
        answerToResponse = {   
                "location_name": self.query,
                "temperature": self.requestWeatherJson['main']['temp'],
                "wind": str(self.requestWeatherJson['wind']['speed']) + "," + str(self.requestWeatherJson['wind']['deg']),
                "cloudiness": self.requestWeatherJson['clouds']['all'],
                "pressure": self.requestWeatherJson['main']['pressure'],
                "humidity": self.requestWeatherJson['main']['humidity'],
                "sunrise": self.requestWeatherJson['sys']['sunrise'],
                "sunset": self.requestWeatherJson['sys']['sunset'],
                "geo_coordinates": str(self.requestWeatherJson['coord']['lat']) + "," + str(self.requestWeatherJson['coord']['lon']),
                "requested_time": datetime.utcnow()
            }
        return answerToResponse