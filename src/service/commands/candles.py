from datetime import datetime, timezone

from src.domain.models import Candle
from src.infrastructure.bybit import ByBitRESTClient, CandleStore
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from src.infrastructure.db.base import session_factory


class CandleCommands:
    @staticmethod
    def get_and_save_candles(store: CandleStore, ticker: str, interval: str = "5", limit: int = 200) -> int:
        # Init ByBitClient
        rest_instance = ByBitRESTClient() 

        # Get klines
        klines = rest_instance.get_klines(ticker, interval, limit)

        # Push to queue
        store.push_many(klines)

        # Save to db
        last_candle_id = None
        with SQLAlchemyUnitOfWork(session_factory) as uow: 
            for kline in klines: 
                timestamp = datetime.fromtimestamp(kline.Timestamp / 1000, tz=timezone.utc)
                candle = Candle(Ticker=ticker, Timeframe=interval, Timestamp=timestamp, Open=float(kline.OpenPrice),
                                High=float(kline.HighPrice), Low=float(kline.LowPrice), Close=float(kline.ClosePrice),
                                Volume=float(kline.Volume))
                last_candle_id = uow.candle_repository.insert(candle.to_dict())

        return last_candle_id
