import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder

class Weather():
    __city = ""
    __country = ""
    __timezone = ""
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
    def getTimezone(self,lon:float,lat:float):
        tf = TimezoneFinder()
        self.__timezone = tf.timezone_at(lng=lon, lat=lat)
        return self.__timezone
    def fromTimestampToLocalDateTime(self,timestamp:int)->str:
        return datetime.fromtimestamp(timestamp).astimezone(ZoneInfo(self.__timezone)).strftime("%Y-%m-%d %H:%M:%S")
