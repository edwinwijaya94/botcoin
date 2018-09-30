import time
from .util import parse_duration, get_config, init_redis
from .indodax import *
from .const import *

def init_cron():
    r = init_redis()
    while True:
        now = int(time.time())
        schedule = get_schedule(r)
        if now < schedule:
            time.sleep(schedule - now)
        track_assets(r)
        schedule = parse_duration(get_config()['cron']['schedule'])
        set_schedule(r, now+schedule)

def get_schedule(r):
    schedule = r.get(REDIS_CRON)
    if schedule:
        return int(schedule.decode("utf-8"))
    return int(0)

def set_schedule(r, schedule_ts):
    r.set(REDIS_CRON, schedule_ts)

def track_assets(r):
    now = int(time.time())
    pair = 'btc_idr'
    price = get_price(pair)
    balance = get_balance(pair.split('_')[0])
    if price >= 0 and balance >= 0 :
        assets = calc_assets(price, balance)

        # store data
        redis_price_key = '{key}:{pair}'.format(key=REDIS_PRICE, pair=pair)
        data = '{price}:{ts}'.format(price=price, ts=now)
        r.zadd(redis_price_key, now, data)
        r.set(REDIS_ASSETS, assets)
        # remove old data
        count = r.zcount(redis_price_key, '-inf', '+inf')
        max_count = get_config()['cron']['price_count']
        if count > max_count:
            r.zremrangebyrank(redis_price_key, 0, count-max_count-1)
