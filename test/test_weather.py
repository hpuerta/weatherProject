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
        response = weather.getResponseData()
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
#1644702000
#Saturday, 12 February 2022 16:40:00
COORDINATES = {
    'lon' : -74.0817,
    'lat' : 4.6097
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

mocked_api_response_url = "https://run.mocky.io/v3/bc90bc9d-3b34-4a02-8a82-ca24b55ee155"
def test_weather_datetime_formatting():
    try:
        weather = Weather(mocked_weather_response_url=mocked_api_response_url,**LOCATION)
        response = weather.getResponseData()
        assert response["location_name"] == "Bogota,co"
        assert response["sunrise"] == "06:11:42"
        assert response["sunset"] == "18:09:36"
        assert response["requested_time"] == "2022-02-12 21:20:01"
    except Exception as e:
        assert False,e


def test_cloudiness_formatting():
    from app.models.textHelper import TextHelper
    assert TextHelper.getCloudinessText(0) == "Sky clear"
    assert TextHelper.getCloudinessText(20) == "Few clouds"
    assert TextHelper.getCloudinessText(40) == "Scattered clouds"
    assert TextHelper.getCloudinessText(70) == "Broken clouds"
    assert TextHelper.getCloudinessText(100) == "Overcast"

@pytest.fixture
def response():
    weather = Weather(mocked_weather_response_url=mocked_api_response_url,**LOCATION)
    return weather.getResponseData()

def test_weather_cloudiness_formatting(response):
    assert response['cloudiness'] == "Broken clouds"

def test_wind_formatting():
    from app.models.textHelper import TextHelper
    assert TextHelper.getWindText(1.5,25) == "Light air, 1.5 m/s, North-Northeast"