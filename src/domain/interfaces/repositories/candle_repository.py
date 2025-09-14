from abc import ABC, abstractmethod
from typing import Iterable

from src.infrastructure.db.models import Candle


class AbstractCandleRepository(ABC):
    @abstractmethod
    def filters(self, filters: dict, one: bool = False) -> Iterable[Candle] | None: ...

    @abstractmethod
    def insert(self, payload: dict) -> int: ...
