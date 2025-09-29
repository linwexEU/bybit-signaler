from src.domain.models import Level
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from src.infrastructure.db.base import session_factory
from src.logger import log


class LevelQueries: 
    @staticmethod
    @log
    def get_levels_by_ticker(ticker: str) -> None: 
        with SQLAlchemyUnitOfWork(session_factory) as uow: 
            levels = uow.level_repository.filters({"Ticker": ticker})
            levels = [Level.from_orm(item) for item in levels]

            if len(levels) < 200: 
                return levels 
            return levels[-200:]
