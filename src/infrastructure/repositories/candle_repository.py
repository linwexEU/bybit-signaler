from typing import Iterable

from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from src.domain.interfaces.repositories import AbstractCandleRepository
from src.infrastructure.db.models import Candle


class CandleRepository(AbstractCandleRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def filters(self, filters: dict, one: bool = False) -> Iterable[Candle] | None:
        query = select(Candle).filter_by(**filters)
        result = self.session.execute(query)

        if one:
            return result.scalar()
        return result.scalars().all()

    def insert(self, payload: dict) -> int:
        query = insert(Candle).values(**payload).returning(Candle.Id)
        result = self.session.execute(query)
        return result.scalar()
