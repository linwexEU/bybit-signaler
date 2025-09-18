from abc import ABC, abstractmethod

import pandas

from src.domain.models import Kline

class AbstractCandleStore(ABC): 
    @abstractmethod
    def push_many(self, klines: list[Kline]) -> None: ...

    @abstractmethod
    def to_dataframe(self) -> pandas.DataFrame: ...
