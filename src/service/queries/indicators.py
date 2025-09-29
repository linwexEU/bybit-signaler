from src.domain.models import Indicator, Candle

from src.infrastructure.db.base import session_factory
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from src.logger import log


class IndicatorQueries: 
    @staticmethod
    @log
    def get_candle_indicators(candles: list[Candle]) -> list[Indicator]: 
        indicators = []
        with SQLAlchemyUnitOfWork(session_factory) as uow: 
            for candle in candles: 
                indicator = uow.indicator_repository.filters({"CandleId": candle.Id})

                if len(indicator) == 1: 
                    indicators.append(Indicator.from_orm(indicator[0]))

        if len(indicators) < 200: 
            return indicators
        return indicators[-200:]
