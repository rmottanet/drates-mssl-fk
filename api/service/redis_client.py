import redis

class RedisClient:
    def __init__(self, host=None, port=None, password=None):
        self.host = host
        self.port = port
        self.password = password

        self.redis_client = redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password
        )

    def get_exrates(self):
        return self.redis_client.hgetall('exrates')
