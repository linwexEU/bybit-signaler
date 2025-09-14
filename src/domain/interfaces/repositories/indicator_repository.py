from abc import ABC, abstractmethod
from typing import Iterable

from src.infrastructure.db.models import Indicator


class AbstractIndicatorRepository(ABC):
    @abstractmethod
    def filters(self, filters: dict, one: bool = False) -> Iterable[Indicator] | None: ...

    @abstractmethod
    def insert(self, payload: dict) -> None: ...
