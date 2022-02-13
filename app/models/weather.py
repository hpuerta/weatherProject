import os
from typing import Dict, List
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
    __API_URL_FORECAST = ""
    __API_KEY = ""
    requestWeatherJson={}
    requestForecastJson={}

    def __init__(self,city:str,country:str,mocked_weather_response_url:str = None,mocked_forecast_response_url:str=None,API_KEY=None)->None:
        self.__city = city
        self.__country = country
        self.query = city + "," + country
        if API_KEY is None:
            self.__API_KEY = os.getenv('API_KEY')
        else:
            self.__API_KEY = API_KEY
        
        if mocked_weather_response_url is None:
            self.__API_URL_WEATHER = f"http://api.openweathermap.org/data/2.5/weather?q={self.query}&units=metric&appid=" + self.__API_KEY
        else:
            self.__API_URL_WEATHER = mocked_weather_response_url

        if mocked_forecast_response_url is None:
            self.__API_URL_FORECAST = f"http://api.openweathermap.org/data/2.5/forecast?q={self.query}&units=metric&appid=" + self.__API_KEY
        else:
            self.__API_URL_FORECAST = mocked_forecast_response_url
    
    def getWeatherJson(self)->None:
        self.requestWeatherJson = requests.get(f"{self.__API_URL_WEATHER}").json()
        try:
            self.getTimezone(self.requestWeatherJson['coord']['lon'],self.requestWeatherJson['coord']['lat'])
        except:
            self.__timezone = "GMT"

    def getForecastJson(self)->None:
        self.requestForecastJson = requests.get(f"{self.__API_URL_FORECAST}").json()

    def getCompleteResponseData(self)->Dict:
        self.getWeatherJson()
        if self.requestWeatherJson.get('main') is None and self.requestWeatherJson.get('message') is not None:
            if self.requestWeatherJson and self.requestWeatherJson.get("message") and self.requestWeatherJson.get("cod"):
                if self.requestWeatherJson.get("cod") == 401:
                    return {'error': "Unexpected error",
                            'status': self.requestWeatherJson.get("cod"),
                            'message': "Invalid API key"}
            return {'error': "Unexpected error",
                    'status': 400,
                    'message': "Unexpected error"}
        self.getForecastJson()
        answerToResponse = {   
                "location_name": self.__city + ", " + self.__country.upper(),
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
        answerToResponse['forecast'] = [self.getIndividualForecastData(forecastElement) for forecastElement in self.requestForecastJson['list']]
        return answerToResponse
    def getTimezone(self,longitude:float,latitude:float)->str:
        tf = TimezoneFinder()
        self.__timezone = tf.timezone_at(lng=longitude, lat=latitude)
        return self.__timezone

    def getIndividualForecastData(self,forecastJson:List)->Dict:
        return {"datetime":DateFormatting.fromTimestampToLocalDateTime(forecastJson['dt'],self.__timezone),
        "temperature": TextHelper.getTemperatureText(forecastJson['main']['temp']),
        "wind": TextHelper.getWindText(forecastJson['wind']['speed'],forecastJson['wind']['deg']),
        "cloudiness": TextHelper.getCloudinessText(forecastJson['clouds']['all']),
        "pressure": TextHelper.getPressureText(forecastJson['main']['pressure']),
        "humidity": TextHelper.getHumidityText(forecastJson['main']['humidity'])}
