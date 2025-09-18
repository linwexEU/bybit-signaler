from src.domain.models import Candle
from src.infrastructure.db.base import session_factory
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork



class CandleQueries: 
    @staticmethod
    def get_candles_by_ticker(ticker: str) -> list[list[Candle]]:
        result = []
        with SQLAlchemyUnitOfWork(session_factory) as uow:
            for timeframe in ["5", "15", "60", "240", "D", "W"]: 
                candles = uow.candle_repository.filters({"Ticker": ticker, "Timeframe": timeframe})
                candles = [Candle.from_orm(candle) for candle in candles]

                if len(candles) < 200:
                    result.append(candles)
                else:
                    result.append(candles[-200:])
        return result
