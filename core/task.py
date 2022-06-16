from config.celery import app
from django.conf import settings
import redis


@app.task
def update_cache(path):
    if path is None:
        return None

    host = settings.REDIS_ADDRESS
    r = redis.StrictRedis(host=host, port=6379, db=0)
    for key in r.scan_iter(f"*{path}*".format(path=path)):
        r.delete(key)

