import redis
import os

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))

r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def is_rate_limited(user_id):
    key = f"rate:{user_id}"
    current = r.get(key)
    if current and int(current) >= 5:
        return True
    else:
        pipe = r.pipeline()
        pipe.incr(key, 1)
        pipe.expire(key, 60)  # reset setelah 60 detik
        pipe.execute()
        return False