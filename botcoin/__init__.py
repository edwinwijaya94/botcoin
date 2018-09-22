import threading
from flask import Flask, jsonify
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
        return jsonify(calc_assets())

    # trans history
    @app.route('/history')
    def history():
        return jsonify(get_transaction_history())

    @app.route('/trade')
    def trade():
        return jsonify(trade_x('btc_idr', 'buy', 10000000, 50000))

    # init cron
    thread = threading.Thread(target=init_cron, args=())
    thread.start()
    thread.join()

    return app
