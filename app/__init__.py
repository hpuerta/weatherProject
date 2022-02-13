from flask import Flask,request,jsonify
import os
from flask_caching import Cache

from app.models.weather import Weather

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        TEST_VAR = os.environ['TEST_VAR'],
        API_KEY = os.environ['API_KEY'],
        MOCKED_WEATHER = None,
        MOCKED_FORECAST = None,
        CACHE_TYPE = os.environ['CACHE_TYPE'],
        CACHE_REDIS_HOST = os.environ['CACHE_REDIS_HOST'],
        CACHE_REDIS_PORT = os.environ['CACHE_REDIS_PORT'],
        CACHE_REDIS_DB = os.environ['CACHE_REDIS_DB'],
        CACHE_REDIS_URL = os.environ['CACHE_REDIS_URL'],
        CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']
    )
    #Check if have any argument for the testing enviroment
    if test_config is not None:
        app.config.from_mapping(test_config)
    
    cache = Cache(app)
    
    @app.route("/weather",methods=['GET'])
    @cache.cached(timeout=120, query_string=True)
    def get_weather():
        country = request.args.get('country')
        city = request.args.get('city')
        temperature_unit = request.args.get('temperature_unit')
        #Check the presence of city in the arguments
        if not (city and city.strip()):
            return jsonify({'error': "Unexpected error",
                    'status': 400,
                    'message': "City is needed"}),400
        #Check the presence of country in the arguments
        if not (country and country.strip()):
            return jsonify({'error': "Unexpected error",
                    'status': 400,
                    'message': "Country is needed"}),400
        #Check the presence of temperature_unit in the arguments
        if temperature_unit!= 'f' and temperature_unit!= 'c':
            temperature_unit = None
        #Check the presence of api-key in the arguments
        api_key = request.args.get('api-key')
        if not api_key:
            api_key = os.getenv('API_KEY')
        weather = Weather(city,
                            country,
                            mocked_weather_response_url=app.config['MOCKED_WEATHER'],
                            mocked_forecast_response_url=app.config['MOCKED_FORECAST'],
                            API_KEY=api_key,
                            temperature_unit=temperature_unit)
        answerToResponse = weather.getCompleteResponseData()
        if answerToResponse.get('status'):
            status_code = int(answerToResponse['status'])
        else:
            status_code = 200
        return jsonify(answerToResponse),status_code
    return app