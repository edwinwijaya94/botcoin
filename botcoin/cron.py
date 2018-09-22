import time
from .util import parse_duration, get_config, init_redis
from .indodax import calc_assets

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
    schedule = r.get('botcoin:cron:schedule')
    if schedule:
        return int(schedule.decode("utf-8"))
    return int(0)

def set_schedule(r, schedule_ts):
    r.set('botcoin:cron:schedule', schedule_ts)

def track_assets(r):
    assets = calc_assets()
    r.set('botcoin:assets', assets)
