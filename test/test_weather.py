def test_import_weather():
    try:
        from app.models.weather import Weather
        assert True
    except Exception as e:
        assert False,e

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
        weather.getTimezone(**COORDINATES)
        response = weather.fromTimestampToLocalDateTime(1644702000)
        assert response == "2022-02-12 16:40:00"
    except Exception as e:
        assert False,e