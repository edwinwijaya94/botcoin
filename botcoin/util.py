import redis
import json

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
