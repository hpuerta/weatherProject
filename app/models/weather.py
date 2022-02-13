import os
from typing import Dict, List
import requests
from timezonefinder import TimezoneFinder
from app.models.dateFormatting import DateFormatting
from app.models.textHelper import TextHelper

class Weather():
    '''This function gets the weather and forecast info from one location and
    returns a dictionary with the information in the required format.
    The principal function is getCompleteResponseData()
    '''
    __city = ""
    __country = ""
    __timezone = ""
    __temperature_unit = None
    query=""
    __API_URL_WEATHER = ""
    __API_URL_FORECAST = ""
    __API_KEY = ""
    requestWeatherJson={}
    requestForecastJson={}

    def __init__(self,city:str,country:str,mocked_weather_response_url:str = None,mocked_forecast_response_url:str=None,API_KEY=None,temperature_unit=None)->None:
        self.__city = city
        self.__country = country
        self.query = city + "," + country
        self.__temperature_unit = temperature_unit
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
        '''This function gets the data of current weather info from https://openweathermap.org API of a given location
        '''
        try:
            self.requestWeatherJson = requests.get(f"{self.__API_URL_WEATHER}").json()
        except:
            self.requestWeatherJson = {'cod': 503,'message': 'Error getting external server'}
        try:
            self.getTimezone(self.requestWeatherJson['coord']['lon'],self.requestWeatherJson['coord']['lat'])
        except:
            self.__timezone = "GMT"

    def getForecastJson(self)->None:
        '''This function gets the data of forecast info from https://openweathermap.org API of a given location
        '''
        try:
            self.requestForecastJson = requests.get(f"{self.__API_URL_FORECAST}").json()
        except:
            self.requestForecastJson = {'cod': 503,'message': 'Error getting external server'}

    def getCompleteResponseData(self)->Dict:
        '''This function creates a dictionary with the required format
        using the data getted from https://openweathermap.org API
            {   
                "location_name": str,
                "temperature": str,
                "wind": str,
                "cloudiness": str,
                "pressure": str,
                "humidity": str,
                "sunrise": str,
                "sunset": str,
                "geo_coordinates": str,
                "requested_time": str
            }
        '''
        self.getWeatherJson()
        if self.requestWeatherJson.get('main') is None and self.requestWeatherJson.get('message') is not None:
            if self.requestWeatherJson and self.requestWeatherJson.get("message") and self.requestWeatherJson.get("cod"):
                if self.requestWeatherJson.get("cod") == 401:
                    return {'error': "Unexpected error",
                            'status': self.requestWeatherJson.get("cod"),
                            'message': "Invalid API key"}
                elif self.requestWeatherJson.get("cod") == 503:
                    return {'error': "Unexpected error",
                            'status': self.requestWeatherJson.get("cod"),
                            'message': self.requestWeatherJson.get("message")}
            return {'error': "Unexpected error",
                    'status': 400,
                    'message': "Unexpected error"}
        self.getForecastJson()
        answerToResponse = {   
                "location_name": self.__city + ", " + self.__country.upper(),
                "temperature": TextHelper.getTemperatureText(self.requestWeatherJson['main']['temp'],temperature_unit=self.__temperature_unit),
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
        '''This function gets the longitude and latitude of one location
        to return the time zone
        '''
        tf = TimezoneFinder()
        self.__timezone = tf.timezone_at(lng=longitude, lat=latitude)
        return self.__timezone

    def getIndividualForecastData(self,forecastJson:List)->Dict:
        '''This gets an individual forecast element from the API to return the formmated dictionary
            {
                "datetime": str,
                "temperature": str,
                "wind": str,
                "cloudiness": str,
                "pressure": str,
                "humidity": str
            }
        '''
        return {"datetime":DateFormatting.fromTimestampToLocalDateTime(forecastJson['dt'],self.__timezone),
        "temperature": TextHelper.getTemperatureText(forecastJson['main']['temp'],temperature_unit=self.__temperature_unit),
        "wind": TextHelper.getWindText(forecastJson['wind']['speed'],forecastJson['wind']['deg']),
        "cloudiness": TextHelper.getCloudinessText(forecastJson['clouds']['all']),
        "pressure": TextHelper.getPressureText(forecastJson['main']['pressure']),
        "humidity": TextHelper.getHumidityText(forecastJson['main']['humidity'])}
