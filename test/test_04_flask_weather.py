import pytest
from app import create_app

CONFIG = {
    'TESTING' : True,
    'MOCKED_WEATHER' : r'https://run.mocky.io/v3/0da14529-078b-4a4e-8f55-b2df81639c8f',
    'MOCKED_FORECAST' : r'https://run.mocky.io/v3/ee44a2f6-353e-406a-bc0a-2462e276501d'
}

def test_get_flask_answer():
    app = create_app(CONFIG)
    response =  app.test_client().get('/weather?city=Bogota&country=co')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert "location_name" in response.get_json().keys()
    assert response.get_json()["location_name"] == "Bogota, CO"
    assert response.get_json()['forecast'][0]['pressure'] == "1022 hpa"
    assert response.get_json()['forecast'][2]['humidity'] == "91%"

@pytest.fixture
def app():
    return create_app({'TESTING':True})
    
def test_use_custom_api_key_flask(app):
    response =  app.test_client().get('/weather?city=Bogota&country=co&api-key=1234')
    assert response.status_code == 401
    assert response.content_type == 'application/json'
    assert "Invalid API key" in response.get_json()['message']

def test_error_city_none_flask(app):
    response =  app.test_client().get('/weather?city=&country=co')
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert response.get_json()['message'] == "City is needed"

def test_error_country_none_flask(app):
    response =  app.test_client().get('/weather?city=Medellin&country=')
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert response.get_json()['message'] == "Country is needed"

def test_temperature_formatting_celius_fahrenheit():
    app = create_app(CONFIG)
    response =  app.test_client().get('/weather?city=Bogota&country=co&temperature_unit=c')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert response.get_json()["temperature"] == "15.73 ºC"
    response =  app.test_client().get('/weather?city=Bogota&country=co&temperature_unit=f')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert response.get_json()["temperature"] == "60.31 ºF"