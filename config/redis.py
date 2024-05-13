import redis
class RedisDB:
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    redis_password = ''
    redis_storage = redis.Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)

    def __init__(self):
        pass

    @classmethod
    def get_redis(cls, key):
        return cls.redis_storage.get(key)

    @classmethod
    def set_redis(cls, key, value):
        cls.redis_storage.set(key, value)

    @classmethod
    def delete_redis(cls, key):
        cls.redis_storage.delete(key)
