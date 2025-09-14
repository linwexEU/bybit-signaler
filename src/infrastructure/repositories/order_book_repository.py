from typing import Iterable

from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from src.domain.interfaces.repositories import AbstractOrderBookRepository
from src.infrastructure.db.models import OrderBook


class OrderBookRepository(AbstractOrderBookRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def filters(self, filters: dict, one: bool = False) -> Iterable[OrderBook] | None:
        query = select(OrderBook).filter_by(**filters)
        result = self.session.execute(query)

        if one:
            return result.scalar()
        return result.scalars().all()

    def insert(self, payload: dict) -> int:
        query = insert(OrderBook).values(**payload).returning(OrderBook.Id)
        result = self.session.execute(query)
        return result.scalar()
