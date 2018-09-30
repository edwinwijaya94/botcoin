# CONST
# redis key
REDIS_PREFIX = 'botcoin'
REDIS_CRON = '{prefix}:cron:schedule'.format(prefix=REDIS_PREFIX)
REDIS_PRICE = '{prefix}:price'.format(prefix=REDIS_PREFIX)
REDIS_ASSETS = '{prefix}:assets'.format(prefix=REDIS_PREFIX)
