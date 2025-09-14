from src.infrastructure.bybit import ByBitRESTClient, ByBitWSClient, CandleStore, SystemManager


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
