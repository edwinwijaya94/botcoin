import redis, json
from collections import namedtuple
from inspect import currentframe, getframeinfo

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

def parse_duration(d):
    val = int(d[:-1])
    time_unit = d[-1:]
    if time_unit == 's':
        return val
    elif time_unit == 'm':
        return val*60
    elif time_unit == 'h':
        return val*60*60

def debug(data):
    frameinfo = getframeinfo(currentframe())
    temp_dirs = frameinfo.filename.split('/')
    filename = temp_dirs[len(temp_dirs)-1]
    print('{filename}:{line}: {data}'.format(filename=filename, line=frameinfo.lineno, data=data))
