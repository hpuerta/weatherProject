import os
import requests
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