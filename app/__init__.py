from cgi import test
from flask import Flask
import os

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        TEST_VAR = os.environ['TEST_VAR'],
        API_KEY = os.environ['API_KEY']
    )

    if test_config is not None:
        app.config.from_mapping(test_config)
        
    return app