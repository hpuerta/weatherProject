from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        TEST_VAR = os.environ['TEST_VAR'],
        API_KEY = os.environ['API_KEY']
    )
    return app