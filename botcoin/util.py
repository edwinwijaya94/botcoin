import redis, json
from collections import namedtuple

config = None

def get_config():
    global config
    if config is None:
        with open('botcoin/config.json', 'r') as f:
            config = json.load(f)
    return config

def init_redis():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    return r

def json_parse(s):
    return json.loads(s, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

def parse_duration(d):
    val = int(d[:-1])
    time_unit = d[-1:]
    if time_unit == "s":
        return val
    elif time_unit == "m":
        return val*60
    elif time_unit == "h":
        return val*60*60
