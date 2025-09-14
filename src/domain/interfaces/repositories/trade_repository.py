from abc import ABC, abstractmethod
from typing import Iterable

from src.infrastructure.db.models import Trade


class AbstractTradeRepository(ABC):
    @abstractmethod
    def filters(self, filters: dict, one: bool = False) -> Iterable[Trade] | None: ...

    @abstractmethod
    def insert(self, payload: dict) -> int: ...
