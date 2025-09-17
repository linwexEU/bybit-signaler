from abc import ABC, abstractmethod

from src.domain.models import Kline, OrderBook, Ticker


class AbstractByBitRESTClient(ABC):
    @abstractmethod
    def get_tickers(self) -> list[Ticker]: ...

    @abstractmethod 
    def get_klines(self, symbol: str, interval: str = "5", limit: int = 200) -> list[Kline]: ...

    @abstractmethod
    def get_order_book(self, symbol: str) -> OrderBook: ...
