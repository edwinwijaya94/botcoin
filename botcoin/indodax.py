import requests, time, urllib, hmac, hashlib, binascii
from .util import get_config, json_parse

def _get_host():
    return get_config()['indodax']['host']

def _get_signature(query):
    secret = get_config()['indodax']['api_secret'].encode()
    message = urllib.parse.urlencode(query)
    signature = hmac.new(secret, message.encode('utf8'), hashlib.sha512).hexdigest()
    return signature

def get_ticker(pair):
    r = requests.get('{host}/api/{pair}/ticker'.format(pair= pair, host=_get_host()))
    res = json_parse(r.text)
    return res

def get_info():
    nonce = int(time.time())
    headers = {'key': get_config()['indodax']['api_key'], 'sign': _get_signature({'method': 'getInfo', 'nonce': nonce})}
    payload = {'method': 'getInfo', 'nonce': nonce}
    r = requests.post('{host}/tapi'.format(host=_get_host()), headers=headers, data=payload)
    # replace reserved keywords
    r_ = r.text.replace('"return"', '"return_"')
    res = json_parse(r_)
    return res

def calc_assets():
    btc_price = get_ticker('btc_idr').ticker.last
    print("BTC price: IDR "+btc_price)
    btc_amt = get_info().return_.balance.btc
    print("BTC amount: "+btc_amt)
    assets = float(btc_price) * float(btc_amt)
    return assets
