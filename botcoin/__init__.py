from flask import Flask
from .indodax import *
from .cron import init_cron

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    @app.route('/')
    def ping():
        return 'OK'

    # calculate assets
    @app.route('/assets')
    def assets():
        return calc_assets()

    # init cron
    init_cron()

    return app
