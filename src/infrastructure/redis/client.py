import redis

import json
from typing import Any

from src.domain.interfaces import AbstractRedisClient
from src.config import settings
from src.logger import log


class RedisClient(AbstractRedisClient): 
    def __init__(self): 
        self.client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    @log
    def get(self, key: str) -> list[dict] | None: 
        payload = self.client.get(key) 
        if payload:
            return json.loads(payload)
        return None

    @log
    def set_key(self, key: str, payload: list[dict]) -> None: 
        payload = json.dumps(payload)
        self.client.set(key, payload) 

    def __enter__(self) -> "RedisClient": 
        return self
    
    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None: 
        if exc_type is None:
            self.client.close()
        