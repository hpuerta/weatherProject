from flask import Flask,request,jsonify
import os

from app.models.weather import Weather

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        TEST_VAR = os.environ['TEST_VAR'],
        API_KEY = os.environ['API_KEY'],
        MOCKED_WEATHER = None,
        MOCKED_FORECAST = None
    )
    
    if test_config is not None:
        app.config.from_mapping(test_config)
    
    @app.route("/weather",methods=['GET'])
    def get_weather():
        country = request.args.get('country')
        city = request.args.get('city')
        #return jsonify(app.config['MOCKED_WEATHER']),200
        weather = Weather(city,country,mocked_weather_response_url=app.config['MOCKED_WEATHER'],mocked_forecast_response_url=app.config['MOCKED_FORECAST'])
        answerToResponse = weather.getResponseData()
        return jsonify(answerToResponse),200
    return app