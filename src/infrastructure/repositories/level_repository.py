from typing import Iterable

from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from src.domain.interfaces.repositories import AbstractLevelRepository
from src.infrastructure.db.models import Level


class LevelRepository(AbstractLevelRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def filters(self, filters: dict, one: bool = False) -> Iterable[Level] | None:
        query = select(Level).filter_by(**filters)
        result = self.session.execute(query)

        if one:
            return result.scalar()
        return result.scalars().all()

    def insert(self, payload: dict) -> int:
        query = insert(Level).values(**payload).returning(Level.Id)
        result = self.session.execute(query)
        return result.scalar()
