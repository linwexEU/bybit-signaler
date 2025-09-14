from abc import ABC, abstractmethod
from typing import Iterable

from src.infrastructure.db.models import OrderBook


class AbstractOrderBookRepository(ABC):
    @abstractmethod
    def filters(self, filters: dict, one: bool = False) -> Iterable[OrderBook] | None: ...

    @abstractmethod
    def insert(self, payload: dict) -> int: ...
