import statistics
from .indodax import *

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

def get_assets_value(pair):
    assets = -1
    price = get_price(pair)
    balance = get_balance(pair.split('_')[0])
    if price >= 0 and balance >=0:
        assets = calc_assets(price, balance)
    return assets

def get_assets_avg_price(currency):
    return 0

# get price history from sorted set data
def filter_data(data):
    res = []
    for k, v in data:
        res.append(float(k.decode().split(':')[0]))
    return res

def is_open_order(pair):
    orders = get_open_orders(pair)
    if 'return_' in orders:
        return len(orders['return_']['orders']) > 0
    return True

# check if current value is far enough from mean
def is_breaking_point(val, mean, type_, threshold):
    if type_ == 'bottom':
        return ((mean - val) / mean) > threshold
    elif type_ == 'top':
        return ((val - mean) / mean) > threshold

def is_profitable(orig_currency, target_currency, current_price, action):
    if action == 'buy':
        return (get_balance(orig_currency) > 0)
    elif action == 'sell':
        return (get_balance(target_currency) > 0) and (current_price > get_assets_avg_price(target_currency))
    return False

def take_decision(pair, data, config):
    orig_currency = pair.split('_')[1] # IDR
    target_currency = pair.split('_')[0] # foreign currency e.g. BTC
    current_price = data[len(data)-1]
    # calculate mean
    mean = statistics.mean(data)
    # take action based on simple moving average alg
    if not is_open_order(pair) and is_breaking_point(current_price, mean, 'bottom', config['bottom_threshold']) and is_profitable(orig_currency, target_currency, current_price, 'buy'):
        print("ACTION: BUY")
        price = current_price * (1 - config.price_multiplier)
        amount = get_balance(orig_currency) * config.amount_multiplier
        do_trade(pair, 'buy', price, amount)
    elif not is_open_order(pair) and is_breaking_point(current_price, mean, 'top', config['top_threshold']) and is_profitable(orig_currency, target_currency, current_price, 'sell'):
        print("ACTION: SELL")
        price = current_price * (1 + config.price_multiplier)
        amount = get_balance(orig_currency) * config.amount_multiplier
        do_trade(pair, 'sell', price, amount)
    return 0
