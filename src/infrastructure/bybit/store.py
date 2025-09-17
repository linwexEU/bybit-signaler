from collections import deque

import pandas

from src.domain.models import Kline
from src.domain.interfaces import AbstractCandleStore 


class CandleStore(AbstractCandleStore):
    def __init__(self): 
        self.queue = deque()

    def push_many(self, klines: list[Kline]) -> None:
        self.queue += klines

    def to_dataframe(self) -> pandas.DataFrame:
        if not self.queue:
            return pandas.DataFrame()

        data = [
            {
                "timestamp": int(k.Timestamp) if k.Timestamp else None,
                "start_time": k.StartTime,
                "open": float(k.OpenPrice),
                "high": float(k.HighPrice),
                "low": float(k.LowPrice),
                "close": float(k.ClosePrice),
                "volume": float(k.Volume),
                "turnover": float(k.Turnover),
                "interval": k.Interval,
                "confirm": k.Confirm
            }
            for k in self.queue
        ]

        dataframe = pandas.DataFrame(data)

        # Sort by time
        dataframe = dataframe.sort_values("timestamp").reset_index(drop=True)
        return dataframe
