
import redis
from django.conf import settings
def redis_conn():
    pool = redis.ConnectionPool(host=settings.REDIS_CONN['HOST'], \
                                port=settings.REDIS_CONN['PORT'],db=settings.REDIS_CONN['DB'],password=settings.REDIS_CONN['PASSWORD'])
    r = redis.Redis(connection_pool=pool)
    return  r

