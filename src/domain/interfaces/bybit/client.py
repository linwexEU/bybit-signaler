from abc import ABC, abstractmethod

from src.domain.models import Kline, Ticker


class AbstractByBitRESTClient(ABC):
    @abstractmethod
    def get_tickers(self) -> list[Ticker]: ...

    @abstractmethod 
    def get_klines(self, symbol: str, interval: str = "5", limit: int = 200) -> list[Kline]: ...


class AbstractByBitWSClient(ABC):
    @abstractmethod
    def handle_message(self, message: dict) -> None: ... 

    @abstractmethod
    def listen(self, symbol: str, interval: int = 5) -> None: ...
