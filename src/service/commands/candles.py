from datetime import datetime, timezone

from src.domain.models import Candle
from src.infrastructure.bybit import ByBitRESTClient
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from src.infrastructure.db.base import session_factory
from src.infrastructure.redis import RedisClient
from src.service.commands.indicators import IndicatorCommands


class CandleCommands:
    @staticmethod
    def get_and_save_candles(ticker: str, interval: str = "5", limit: int = 200) -> int:
        # Init ByBitClient
        rest_instance = ByBitRESTClient() 

        # Get klines
        klines = rest_instance.get_klines(ticker, interval, limit)

        # Save klines to Redis
        with RedisClient() as redis_client: 
            klines_from_redis = redis_client.get(ticker)
            if klines_from_redis:
                redis_client.set_key(ticker, [item.to_dict() for item in klines] + klines_from_redis)
            else:
                redis_client.set_key(ticker, [item.to_dict() for item in klines])

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
