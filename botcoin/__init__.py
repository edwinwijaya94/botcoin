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

    @app.route('/assets')
    def assets():
        return jsonify(calc_assets())

    @app.route('/transaction/history')
    def transaction_history():
        return jsonify(get_transaction_history())

    @app.route('/trade')
    def trade():
        return jsonify(do_trade('btc_idr', 'buy', 10000000, 50000))

    @app.route('/trade/history')
    def trade_history():
        return jsonify(get_trade_history('btc_idr'))

    # init cron
    thr = threading.Thread(target=init_cron, args=())
    thr.start()
    thr.join()

    return app
