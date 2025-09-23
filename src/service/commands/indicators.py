from src.infrastructure.bybit import SystemManager
from src.infrastructure.db.base import session_factory 
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork


class IndicatorCommands: 
    @staticmethod
    def get_and_save_indicators(ticker: str, interval: str, candle_id: int) -> None: 
        # Get dataframe
        dataframe = SystemManager.to_dataframe(ticker)

        # Calculate indicator
        indicator = SystemManager.calculate_indicators(dataframe, interval, candle_id)

        # Save to Db
        with SQLAlchemyUnitOfWork(session_factory) as uow: 
            uow.indicator_repository.insert(indicator.to_dict())
