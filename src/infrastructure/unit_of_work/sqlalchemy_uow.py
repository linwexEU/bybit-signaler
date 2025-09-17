from typing import Any

from sqlalchemy.orm import Session, sessionmaker

from src.domain.interfaces.unit_of_work import AbstractUnitOfWork
from src.infrastructure.repositories import CandleRepository, IndicatorRepository, LevelRepository, OrderBookRepository


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session: Session = session_factory()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def __enter__(self) -> "SQLAlchemyUnitOfWork":
        self.candle_repository = CandleRepository(self.session)
        self.indicator_repository = IndicatorRepository(self.session)
        self.level_repository = LevelRepository(self.session)
        self.order_book_repository = OrderBookRepository(self.session)
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
