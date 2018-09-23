import threading
from flask import Flask, jsonify
from .indodax import *
from .cron import init_cron

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    @app.route('/')
    def ping_handler():
        return 'OK'

    @app.route('/assets')
    def assets_handler():
        return jsonify(calc_assets())

    @app.route('/transaction/history')
    def transaction_history_handler():
        return jsonify(get_transaction_history())

    @app.route('/trade')
    def trade_handler():
        return jsonify(do_trade('btc_idr', 'buy', 10000000, 50000))

    @app.route('/trade/history')
    def trade_history_handler():
        return jsonify(get_trade_history('btc_idr'))

    @app.route('/order/open')
    def open_orders_handler():
        return jsonify(get_open_orders('btc_idr'))

    @app.route('/order/history')
    def order_history_handler():
        return jsonify(get_order_history('btc_idr'))

    @app.route('/order/detail/<id>')
    def order_detail_handler(id):
        return jsonify(get_order_detail('btc_idr', id))

    @app.route('/order/cancel/<id>')
    def cancel_order_handler(id):
        return jsonify(cancel_order('btc_idr', id, 'buy'))

    # init cron
    thr = threading.Thread(target=init_cron, args=())
    thr.start()
    thr.join()

    return app
