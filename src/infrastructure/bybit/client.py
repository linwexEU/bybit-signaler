from pybit.unified_trading import HTTP

from src.config import settings
from src.domain.interfaces import AbstractByBitRESTClient, AbstractByBitWSClient
from src.domain.models import Kline, Ticker
from src.infrastructure.bybit.system_manager import SystemManager


class ByBitClient(AbstractByBitRESTClient): 
    def __init__(self) -> None: 
        self.session = HTTP(testnet=False, api_key=settings.API_KEY, api_secret=settings.API_SECRET)
    
    def get_tickers(self) -> list[Ticker]:
        tickers = self.session.get_tickers(category="linear")
        return [Ticker.build_obj(item) for item in tickers.get("result").get("list")]
    
    def get_klines(self, symbol: str, interval: str = "5", limit: int = 200) -> list[Kline]: 
        klines = self.session.get_kline(symbol=symbol, interval=interval, limit=limit)
        return [Kline.build_obj(item) for item in klines.get("result").get("list")]
    

class ByBitWSClient(AbstractByBitWSClient): 
    pass


if __name__ == "__main__": 
    client = ByBitClient()

    tickers = client.get_tickers()
    print(SystemManager.get_active_tickers(tickers, settings.THRESHOLD))
