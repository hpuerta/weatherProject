from app.models.textHelper import TextHelper
def test_cloudiness_formatting():
    try:
        assert TextHelper.getCloudinessText(0) == "Sky clear"
        assert TextHelper.getCloudinessText(20) == "Few clouds"
        assert TextHelper.getCloudinessText(40) == "Scattered clouds"
        assert TextHelper.getCloudinessText(70) == "Broken clouds"
        assert TextHelper.getCloudinessText(100) == "Overcast"
    except Exception as e:
        assert False,e

def test_wind_formatting():
    try:
        assert TextHelper.getWindText(1.5,25) == "Light air, 1.5 m/s, North-Northeast"
    except Exception as e:
        assert False,e

def test_pressure_formatting():
    try:
        assert TextHelper.getPressureText(1010) == "1010 hpa"
    except Exception as e:
        assert False,e

def test_humidity_formatting():
    try:
        assert TextHelper.getHumidityText(40) == "40%"
    except Exception as e:
        assert False,e

def test_coordinates_formatting():
    try:
        assert TextHelper.getCoordinatesText(40,50) == "[40, 50]"
    except Exception as e:
        assert False,e

def test_temperature_formatting():
    try:
        assert TextHelper.getTemperatureText(30) == "30 ºC / 86 ºF"
    except Exception as e:
        assert False,e