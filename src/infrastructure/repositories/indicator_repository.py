from typing import Iterable

from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from src.domain.interfaces.repositories import AbstractIndicatorRepository
from src.infrastructure.db.models import Indicator


class IndicatorRepository(AbstractIndicatorRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def filters(self, filters: dict, one: bool = False) -> Iterable[Indicator] | None:
        query = select(Indicator).filter_by(**filters)
        result = self.session.execute(query)

        if one:
            return result.scalar()
        return result.scalars().all()

    def insert(self, payload: dict) -> int:
        query = insert(Indicator).values(**payload).returning(Indicator.Id)
        result = self.session.execute(query)
        return result.scalar()
