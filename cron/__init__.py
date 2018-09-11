from flask import Flask
from .indodax import *


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # a simple page that says hello
    @app.route('/')
    def ping():
        return 'OK'

    # call indodax api
    @app.route('/assets')
    def assets():
        return calc_assets()

    return app
