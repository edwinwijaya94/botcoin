import requests, time, urllib, hmac, hashlib, binascii, json
from collections import namedtuple

def _get_signature(query):
    key = b'49f84cbcf03154df10c5c2b06623c0ea343964ebc4c2b65cb2ea955a754ca11a86ef964720bb15e4'
    message = urllib.parse.urlencode(query)
    signature = hmac.new(key, message.encode('utf8'), hashlib.sha512).hexdigest()
    return signature

def get_ticker(pair):
    r = requests.get('https://indodax.com/api/{pair}/ticker'.format(pair= pair))
    res = json.loads(r.text, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return res

def get_info():
    nonce = int(time.time())
    headers = {'key': 'K7VW3JUX-3SHFWP5V-FEKZPD0T-JN8VW8ME-RORZBQMH', 'sign': _get_signature({'method': 'getInfo', 'nonce': nonce})}
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
    res = "BTC assets: IDR "+str(assets)
    return res
