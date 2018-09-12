import requests, time, urllib, hmac, hashlib, binascii, json
from collections import namedtuple
from .util import get_config

def _get_signature(query):
    secret = get_config()['indodax']['api_secret'].encode()
    message = urllib.parse.urlencode(query)
    signature = hmac.new(secret, message.encode('utf8'), hashlib.sha512).hexdigest()
    return signature

def get_ticker(pair):
    r = requests.get('https://indodax.com/api/{pair}/ticker'.format(pair= pair))
    res = json.loads(r.text, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return res

def get_info():
    nonce = int(time.time())
    headers = {'key': get_config()['indodax']['api_key'], 'sign': _get_signature({'method': 'getInfo', 'nonce': nonce})}
    payload = {'method': 'getInfo', 'nonce': nonce}
    r = requests.post('https://indodax.com/tapi', headers=headers, data=payload)
    # replace reserved keywords
    r_ = r.text.replace('"return"', '"return_"')
    res = json.loads(r_, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return res

def calc_assets():
    btc_price = get_ticker('btc_idr').ticker.last
    print("BTC price: IDR "+btc_price)
    btc_amt = get_info().return_.balance.btc
    print("BTC amount: "+btc_amt)
    assets = float(btc_price) * float(btc_amt)
    return assets
