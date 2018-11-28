import redis
from django.conf import settings
import json
import os
def redis_conn():
    pool = redis.ConnectionPool(host=settings.REDIS_CONN['HOST'], port=settings.REDIS_CONN['PORT'],db=settings.REDIS_CONN['DB'],password='meiyoumima')
    r = redis.Redis(connection_pool=pool)
    return  r

# r=redis_conn()
#
# r.set('img',json.dumps())