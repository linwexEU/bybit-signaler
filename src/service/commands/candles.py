from datetime import datetime, timezone

from src.domain.models import Candle
from src.infrastructure.bybit import ByBitRESTClient, ByBitWSClient, CandleStore, SystemManager
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from src.infrastructure.db.base import session_factory


class CandleService:
    def __init__(self) -> None:
        self.rest_instance = ByBitRESTClient()
        self.ws_instance = ByBitWSClient()
        self.store = CandleStore()

    def save_candles(self, symbol: str, interval: str = "5", limit: int = 200) -> None:
        # Get klines
        klines = self.rest_instance.get_klines(symbol, interval, limit)

        # Push to queue
        self.store.push_many(klines)

        # Save to db
        last_candle_id = None
        with SQLAlchemyUnitOfWork(session_factory) as uow:
            for kline in klines:
                timestamp = datetime.fromtimestamp(kline.Timestamp / 1000, tz=timezone.utc)
                candle = Candle(Ticker=symbol, Timeframe=interval, Timestamp=timestamp, Open=float(kline.OpenPrice),
                                High=float(kline.HighPrice), Low=float(kline.LowPrice), Close=float(kline.ClosePrice),
                                Volume=float(kline.Volume))
                print(candle)
                last_candle_id = uow.candle_repository.insert(candle.to_dict())

        # Create dataframe
        dataframe = self.store.to_dataframe()

        # Calculate Indicator
        indicator = SystemManager.calculate_indicators(dataframe, last_candle_id)
        print(indicator)


if __name__ == "__main__":
    candle_service = CandleService()
    candle_service.save_candles("ETHUSDT")
