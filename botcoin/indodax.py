import requests, time, urllib, hmac, hashlib, json
from .util import get_config

# helper functions
def _get_host():
    return get_config()['indodax']['host']

def _get_tapi_url():
    return '{host}/tapi'.format(host=_get_host())

def _get_signature(query):
    secret = get_config()['indodax']['api_secret'].encode()
    message = urllib.parse.urlencode(query)
    signature = hmac.new(secret, message.encode('utf8'), hashlib.sha512).hexdigest()
    return signature

# public APIs
def get_ticker(pair):
    r = requests.get('{host}/api/{pair}/ticker'.format(pair= pair, host=_get_host()))
    res = json.loads(r.text)
    return res

# private APIs
def get_info():
    method = 'getInfo'
    nonce = int(time.time())
    headers = {'key': get_config()['indodax']['api_key'], 'sign': _get_signature({'method': method, 'nonce': nonce})}
    payload = {'method': method, 'nonce': nonce}
    r = requests.post(_get_tapi_url(), headers=headers, data=payload)
    # replace reserved keywords
    r_ = r.text.replace('"return"', '"return_"')
    res = json.loads(r_)
    return res

def get_transaction_history():
    method = 'transHistory'
    nonce = int(time.time())
    headers = {'key': get_config()['indodax']['api_key'], 'sign': _get_signature({'method': method, 'nonce': nonce})}
    payload = {'method': method, 'nonce': nonce}
    r = requests.post(_get_tapi_url(), headers=headers, data=payload)
    # replace reserved keywords
    r_ = r.text.replace('"return"', '"return_"')
    res = json.loads(r_)
    return res

def do_trade(pair, action, price, amount):
    method = 'trade'
    nonce = int(time.time())
    payload = {'method': method, 'nonce': nonce, 'pair': pair, 'type': action, 'price': price, 'idr': amount}
    headers = {'key': get_config()['indodax']['api_key'], 'sign': _get_signature(payload)}
    r = requests.post(_get_tapi_url(), headers=headers, data=payload)
    # replace reserved keywords
    r_ = r.text.replace('"return"', '"return_"')
    res = json.loads(r_)
    return res

def get_trade_history(pair):
    method = 'tradeHistory'
    nonce = int(time.time())
    payload = {'method': method, 'nonce': nonce, 'pair': pair}
    headers = {'key': get_config()['indodax']['api_key'], 'sign': _get_signature(payload)}
    r = requests.post(_get_tapi_url(), headers=headers, data=payload)
    # replace reserved keywords
    r_ = r.text.replace('"return"', '"return_"')
    res = json.loads(r_)
    return res

def get_open_orders(pair):
    method = 'openOrders'
    nonce = int(time.time())
    payload = {'method': method, 'nonce': nonce, 'pair': pair}
    headers = {'key': get_config()['indodax']['api_key'], 'sign': _get_signature(payload)}
    r = requests.post(_get_tapi_url(), headers=headers, data=payload)
    # replace reserved keywords
    r_ = r.text.replace('"return"', '"return_"')
    res = json.loads(r_)
    return res

def get_order_history(pair):
    method = 'orderHistory'
    nonce = int(time.time())
    payload = {'method': method, 'nonce': nonce, 'pair': pair}
    headers = {'key': get_config()['indodax']['api_key'], 'sign': _get_signature(payload)}
    r = requests.post(_get_tapi_url(), headers=headers, data=payload)
    # replace reserved keywords
    r_ = r.text.replace('"return"', '"return_"')
    res = json.loads(r_)
    return res

def get_order_detail(pair, id):
    method = 'getOrder'
    nonce = int(time.time())
    payload = {'method': method, 'nonce': nonce, 'pair': pair, 'order_id': id}
    headers = {'key': get_config()['indodax']['api_key'], 'sign': _get_signature(payload)}
    r = requests.post(_get_tapi_url(), headers=headers, data=payload)
    # replace reserved keywords
    r_ = r.text.replace('"return"', '"return_"')
    res = json.loads(r_)
    return res

def cancel_order(pair, id, action):
    method = 'cancelOrder'
    nonce = int(time.time())
    payload = {'method': method, 'nonce': nonce, 'pair': pair, 'order_id': id, 'type': action}
    headers = {'key': get_config()['indodax']['api_key'], 'sign': _get_signature(payload)}
    r = requests.post(_get_tapi_url(), headers=headers, data=payload)
    # replace reserved keywords
    r_ = r.text.replace('"return"', '"return_"')
    res = json.loads(r_)
    return res

# calc functions
def get_price(pair):
    data = get_ticker(pair)
    price = -1
    if 'ticker' in data:
        price = data['ticker']['last']
    return float(price)

def get_balance(currency):
    data = get_info()
    balance = -1
    if 'return_' in data:
        balance = data['return_']['balance'][currency]
    return float(balance)

def calc_assets(price, balance):
    return price * balance

def get_assets(pair):
    assets = -1
    price = get_price(pair)
    balance = get_balance(pair.split('_')[0])
    if price >= 0 and balance >=0:
        assets = calc_assets(price, balance)
    return assets
