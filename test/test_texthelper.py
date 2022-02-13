from app.models.textHelper import TextHelper
def test_cloudiness_formatting():
    assert TextHelper.getCloudinessText(0) == "Sky clear"
    assert TextHelper.getCloudinessText(20) == "Few clouds"
    assert TextHelper.getCloudinessText(40) == "Scattered clouds"
    assert TextHelper.getCloudinessText(70) == "Broken clouds"
    assert TextHelper.getCloudinessText(100) == "Overcast"

def test_wind_formatting():
    assert TextHelper.getWindText(1.5,25) == "Light air, 1.5 m/s, North-Northeast"

def test_pressure_formatting():
    assert TextHelper.getPressureText(1010) == "1010 hpa"

def test_humidity_formatting():
    assert TextHelper.getHumidityText(40) == "40%"

def test_coordinates_formatting():
    assert TextHelper.getCoordinatesText(40,50) == "[40, 50]"

def test_temperature_formatting():
    assert TextHelper.getTemperatureText(30) == "30 ºC / 86 ºF"