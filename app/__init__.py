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
    
    if test_config is not None:
        app.config.from_mapping(test_config)
    cache = Cache(app)
    @app.route("/weather",methods=['GET'])
    @cache.cached(timeout=120, query_string=True)
    def get_weather():
        country = request.args.get('country')
        city = request.args.get('city')
        api_key = request.args.get('api-key')
        weather = Weather(city,country,mocked_weather_response_url=app.config['MOCKED_WEATHER'],mocked_forecast_response_url=app.config['MOCKED_FORECAST'],API_KEY=api_key)
        answerToResponse = weather.getCompleteResponseData()
        if answerToResponse.get('status'):
            status_code = int(answerToResponse['status'])
        else:
            status_code = 200
        return jsonify(answerToResponse),status_code
    return app