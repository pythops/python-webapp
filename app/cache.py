import redis.asyncio as redis
from redis.asyncio.client import Redis


class Cache:
    def __init__(self):
        self._client: Redis | None = None
        self.test = None

    def __getattr__(self, name):
        return getattr(self._client, name)

    def init(self, host: str, port: int, password: str, db: str):
        self._client = redis.from_url(
            f"redis://{host}",
            port=port,
            password=password,
            db=db,
            socket_connect_timeout=2.0,
            encoding="utf-8",
            decode_responses=True,
        )


cache = Cache()
