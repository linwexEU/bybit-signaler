from abc import ABC, abstractmethod


class AbstractRedisClient(ABC):
    @abstractmethod 
    def get(self, key: str) -> list[dict] | None: ...

    @abstractmethod
    def set_key(self, key: str, payload: dict) -> None: ...
