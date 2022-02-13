from app import create_app

CONFIG = {
    'TESTING' : True,
    'MOCKED_WEATHER' : r'https://run.mocky.io/v3/0da14529-078b-4a4e-8f55-b2df81639c8f',
    'MOCKED_FORECAST' : r'https://run.mocky.io/v3/ee44a2f6-353e-406a-bc0a-2462e276501d'
}

def test_get_answer():
    app = create_app(CONFIG)
    response =  app.test_client().get('/weather?city=Bogota&country=co')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert "location_name" in response.get_json().keys()
    assert response.get_json()["location_name"] == "Bogota, CO"
    assert response.get_json()['forecast'][0]['pressure'] == "1022 hpa"
    assert response.get_json()['forecast'][2]['humidity'] == "91%"