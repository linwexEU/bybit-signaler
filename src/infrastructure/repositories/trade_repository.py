from typing import Iterable

from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from src.domain.interfaces.repositories import AbstractTradeRepository
from src.infrastructure.db.models import Trade


class TradeRepository(AbstractTradeRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def filters(self, filters: dict, one: bool = False) -> Iterable[Trade] | None:
        query = select(Trade).filter_by(**filters)
        result = self.session.execute(query)

        if one:
            return result.scalar()
        return result.scalars().all()

    def insert(self, payload: dict) -> None:
        query = insert(Trade).values(**payload)
        self.session.execute(query)
