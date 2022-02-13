import os
import requests
from timezonefinder import TimezoneFinder
from app.models.dateFormatting import DateFormatting
from app.models.textHelper import TextHelper

class Weather():
    __city = ""
    __country = ""
    __timezone = ""
    query=""
    __API_URL_WEATHER = ""
    requestWeatherJson={}

    def __init__(self,city:str,country:str,mocked_weather_response_url = None)->None:
        self.__city = city
        self.__country = country
        self.query = city + "," + country
        if mocked_weather_response_url is None:
            self.__API_URL_WEATHER = f"http://api.openweathermap.org/data/2.5/weather?q={self.query}&units=metric&appid=" + os.getenv("API_KEY")
        else:
            self.__API_URL_WEATHER = mocked_weather_response_url
    
    def getWeatherJson(self):
        self.requestWeatherJson = requests.get(f"{self.__API_URL_WEATHER}").json()
        self.getTimezone(self.requestWeatherJson['coord']['lon'],self.requestWeatherJson['coord']['lat'])

    def getResponseData(self):
        self.getWeatherJson()
        answerToResponse = {   
                "location_name": self.query,
                "temperature": TextHelper.getTemperatureText(self.requestWeatherJson['main']['temp']),
                "wind": TextHelper.getWindText(self.requestWeatherJson['wind']['speed'],self.requestWeatherJson['wind']['deg']),
                "cloudiness": TextHelper.getCloudinessText(self.requestWeatherJson['clouds']['all']),
                "pressure": TextHelper.getPressureText(self.requestWeatherJson['main']['pressure']),
                "humidity": TextHelper.getHumidityText(self.requestWeatherJson['main']['humidity']),
                "sunrise": DateFormatting.fromTimestampToLocalTime(self.requestWeatherJson['sys']['sunrise'],self.__timezone),
                "sunset": DateFormatting.fromTimestampToLocalTime(self.requestWeatherJson['sys']['sunset'],self.__timezone),
                "geo_coordinates": TextHelper.getCoordinatesText(self.requestWeatherJson['coord']['lat'],self.requestWeatherJson['coord']['lon']),
                "requested_time": DateFormatting.fromTimestampToLocalDateTime(self.requestWeatherJson['dt'],"GMT")
            }
        return answerToResponse
    def getTimezone(self,lon:float,lat:float):
        tf = TimezoneFinder()
        self.__timezone = tf.timezone_at(lng=lon, lat=lat)
        return self.__timezone
