from abc import ABC, abstractmethod
from typing import Iterable

from src.infrastructure.db.models import Level


class AbstractLevelRepository(ABC):
    @abstractmethod
    def filters(self, filters: dict, one: bool = False) -> Iterable[Level] | None: ...

    @abstractmethod
    def insert(self, payload: dict) -> int: ...
