import time

from pybit.unified_trading import HTTP, WebSocket

from src.config import settings
from src.domain.interfaces import AbstractByBitRESTClient, AbstractByBitWSClient
from src.domain.models import Kline, Ticker
from src.infrastructure.bybit.system_manager import SystemManager


class ByBitRESTClient(AbstractByBitRESTClient): 
    def __init__(self) -> None: 
        self.session = HTTP(testnet=False, api_key=settings.API_KEY, api_secret=settings.API_SECRET)
    
    def get_tickers(self) -> list[Ticker]:
        tickers = self.session.get_tickers(category="linear")
        return [Ticker.build_obj(item) for item in tickers.get("result").get("list")]
    
    def get_klines(self, symbol: str, interval: str = "5", limit: int = 200) -> list[Kline]: 
        klines = self.session.get_kline(symbol=symbol, interval=interval, limit=limit)
        return [Kline.build_obj(item, klines.get("time")) for item in klines.get("result").get("list")]
    

class ByBitWSClient(AbstractByBitWSClient): 
    def __init__(self) -> None: 
        self.ws_client = WebSocket(testnet=False, channel_type="linear", api_key=settings.API_KEY, api_secret=settings.API_SECRET)
    
    def handle_message(self, message: dict) -> None: 
        if "topic" in message and "kline" in message["topic"]:
            kline = Kline.build_from_dict(message["data"][0])
            print(kline)

    def listen(self, symbol: str, interval: int = 5) -> None: 
        self.ws_client.kline_stream(interval=interval, symbol=symbol, callback=self.handle_message)


if __name__ == "__main__":
    rest_client_instance = ByBitRESTClient()
    ws_client_instance  = ByBitWSClient()
    # ws_client_instance.listen("ALPHAUSDT")
    
    print(rest_client_instance.get_klines("ZORAUSDT"))
    # try:
    #     while True: 
    #         time.sleep(0.3)
    # except KeyboardInterrupt: 
    #     pass 
