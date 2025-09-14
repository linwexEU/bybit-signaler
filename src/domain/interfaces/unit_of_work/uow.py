from abc import ABC, abstractmethod
from typing import Any

from src.domain.interfaces.repositories import AbstractCandleRepository, AbstractIndicatorRepository, \
                                               AbstractLevelRepository, AbstractOrderBookRepository, \
                                               AbstractTradeRepository


class AbstractUnitOfWork(ABC):
    candle_repository: AbstractCandleRepository
    indicator_repository: AbstractIndicatorRepository
    level_repository: AbstractLevelRepository
    order_book_repository: AbstractOrderBookRepository
    trade_repository: AbstractTradeRepository

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...

    def __enter__(self) -> "AbstractUnitOfWork": ...

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None: ...
