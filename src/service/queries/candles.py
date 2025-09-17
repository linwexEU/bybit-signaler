from src.domain.models import Candle
from src.infrastructure.db.base import session_factory
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork



class CandleQueries: 
    @staticmethod
    def get_candles_by_ticker(ticker: str) -> list[Candle]:
        with SQLAlchemyUnitOfWork(session_factory) as uow: 
            candles = uow.candle_repository.filters({"Ticker": ticker})
            candles = [Candle.from_orm(candle) for candle in candles]

            if len(candles) < 200:
                return candles
            return candles[-200:]
