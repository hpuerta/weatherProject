def test_import_weather():
    try:
        from app.models.weather import Weather
        assert True
    except Exception as e:
        assert False,e

import pytest
from app.models.weather import Weather
def test_weather_init():
    try:
        City = 'Bogota'
        Country = 'co'
        weather = Weather(city=City,country=Country)
        assert weather.query == 'Bogota,co'
    except Exception as e:
        assert False,e
LOCATION = {
    'city' : 'Bogota',
    'country' : 'co'
}
def test_get_weather_api_data_json():
    try:
        weather = Weather(**LOCATION)
        weather.getWeatherJson()
        response = weather.requestWeatherJson
        assert "visibility" in response.keys()
        assert response["name"] == "Bogota"
    except Exception as e:
        assert False,e

def test_get_now_data_basic_formated():
    try:
        weather = Weather(**LOCATION)
        response = weather.getCompleteResponseData()
        assert "location_name" in response.keys()
        assert "temperature" in response.keys()
        assert "wind" in response.keys()
        assert "cloudiness" in response.keys()
        assert "pressure" in response.keys()
        assert "humidity" in response.keys()
        assert "sunrise" in response.keys()
        assert "sunset" in response.keys()
        assert "geo_coordinates" in response.keys()
        assert "requested_time" in response.keys()
    except Exception as e:
        assert False,e

COORDINATES = {
    'longitude' : -74.0817,
    'latitude' : 4.6097
}
def test_get_timezone():
    try:
        weather = Weather(**LOCATION)
        response = weather.getTimezone(**COORDINATES)
        assert response == 'America/Bogota'
    except Exception as e:
        assert False,e
def test_date_format():
    try:
        weather = Weather(**LOCATION)
        timezone = weather.getTimezone(**COORDINATES)
        from app.models.dateFormatting import DateFormatting
        response = DateFormatting.fromTimestampToLocalDateTime(1644702000,timezone)
        assert response == "2022-02-12 16:40:00"
    except Exception as e:
        assert False,e

def test_hour_format():
    try:
        weather = Weather(**LOCATION)
        timezone = weather.getTimezone(**COORDINATES)
        from app.models.dateFormatting import DateFormatting
        response = DateFormatting.fromTimestampToLocalTime(1644702000,timezone)
        assert response == "16:40:00"
    except Exception as e:
        assert False,e

mocked_weather_response_url = "https://run.mocky.io/v3/0da14529-078b-4a4e-8f55-b2df81639c8f"
mocked_forecast_response_url = "https://run.mocky.io/v3/ee44a2f6-353e-406a-bc0a-2462e276501d"
@pytest.fixture
def response():
    try:
        weather = Weather(mocked_weather_response_url=mocked_weather_response_url,mocked_forecast_response_url=mocked_forecast_response_url,**LOCATION)
        return weather.getCompleteResponseData()
    except:
        return None

def test_weather_datetime_formatting(response):
    try:
        assert response["location_name"] == "Bogota, CO"
        assert response["sunrise"] == "06:11:42"
        assert response["sunset"] == "18:09:36"
        assert response["requested_time"] == "2022-02-12 23:29:02 GMT"
    except Exception as e:
        assert False,e

def test_weather_cloudiness_formatting(response):
    try:
        assert response['cloudiness'] == "Broken clouds"
    except Exception as e:
        assert False,e

def test_weather_wind_formatting(response):
    try:
        assert response['wind'] == "Gentle breeze, 4.12 m/s, West"
    except Exception as e:
        assert False,e

def test_weather_pressure_formatting(response):
    try:
        assert response['pressure'] == "1023 hpa"
    except Exception as e:
        assert False,e

def test_weather_humidity_formatting(response):
    try:
        assert response['humidity'] == "72%"
    except Exception as e:
        assert False,e

def test_weather_coordinates_formatting(response):
    try:
        assert response['geo_coordinates'] == "[4.61, -74.08]"
    except Exception as e:
        assert False,e

def test_weather_temperature_formatting(response):
    try:
        assert response['temperature'] == "15.73 ºC / 60.31 ºF"
    except Exception as e:
        assert False,e

def test_get_forecast_api_data_json():
    try:
        weather = Weather(**LOCATION)
        weather.getForecastJson()
        response = weather.requestForecastJson
        assert "list" in response.keys()
        assert response["city"]["name"] == "Bogota"
    except Exception as e:
        assert False,e

def test_get_forecast_data_formatted(response):
    try:
        assert "temperature" in response['forecast'][0].keys()
        assert "wind" in response['forecast'][0].keys()
        assert "cloudiness" in response['forecast'][0].keys()
        assert "pressure" in response['forecast'][0].keys()
        assert "humidity" in response['forecast'][0].keys()
        assert "datetime" in response['forecast'][0].keys()
    except Exception as e:
        assert False,e
CUSTOM_API_KEY = "MY CUSTOM API KEY"
def test_use_custom_api_key():
    try:
        weather = Weather(API_KEY=CUSTOM_API_KEY,**LOCATION)
        assert "Invalid API key" in weather.getCompleteResponseData()['message']
    except Exception as e:
        assert False,e

def test_weather_temperature_celcius_formatting():
    try:
        weather = Weather(temperature_unit='c',mocked_weather_response_url=mocked_weather_response_url,mocked_forecast_response_url=mocked_forecast_response_url,**LOCATION)
        response = weather.getCompleteResponseData()
        assert response['temperature'] == "15.73 ºC"
    except Exception as e:
        assert False,e

def test_weather_temperature_fahrenheit_formatting():
    try:
        weather = Weather(temperature_unit='f',mocked_weather_response_url=mocked_weather_response_url,mocked_forecast_response_url=mocked_forecast_response_url,**LOCATION)
        response = weather.getCompleteResponseData()
        assert response['temperature'] == "60.31 ºF"
    except Exception as e:
        assert False,e