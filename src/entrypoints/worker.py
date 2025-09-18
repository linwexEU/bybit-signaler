from src.infrastructure.bybit import CandleStore
from src.service.commands import CandleCommands, IndicatorCommands, LevelCommands



class Worker: 
    def __init__(self): 
        self.store_5 = CandleStore()  # 5 TF
        self.store_30 = CandleStore() # 30 TF
        self.store_60 = CandleStore() # 1h TF
        self.store_240 = CandleStore() # 4h TF
        self.store_1d = CandleStore() # 1d TF
        self.store_1w = CandleStore() # 1w TF

    def collecting_candles_and_indicators(self, ticker: str, interval: str):
        if interval == "5":
            candle_id = CandleCommands.get_and_save_candles(self.store_5, ticker, interval=interval)
            IndicatorCommands.get_and_save_indicators(self.store_5, interval, candle_id)
        elif interval == "15":
            candle_id = CandleCommands.get_and_save_candles(self.store_15, ticker, interval=interval)
            IndicatorCommands.get_and_save_indicators(self.store_15, interval, candle_id)
        elif interval == "60": 
            candle_id = CandleCommands.get_and_save_candles(self.store_60, ticker, interval=interval)
            IndicatorCommands.get_and_save_indicators(self.store_60, interval, candle_id)
        elif interval == "D":
            candle_id = CandleCommands.get_and_save_candles(self.store_1d, ticker, interval=interval)
            IndicatorCommands.get_and_save_indicators(self.store_1d, interval, candle_id)
        elif interval == "W": 
            candle_id = CandleCommands.get_and_save_candles(self.store_1w, ticker, interval=interval)
            IndicatorCommands.get_and_save_indicators(self.store_1w, interval, candle_id)
        else: 
            candle_id = CandleCommands.get_and_save_candles(self.store_240, ticker, interval=interval)
            IndicatorCommands.get_and_save_indicators(self.store_240, interval, candle_id)

    def collecting_levels(self, ticker: str): 
        LevelCommands.get_and_save_levels(ticker)


if __name__ == "__main__": 
    worker = Worker()
    worker.collecting_candles_and_indicators("SOLUSDT", "5")
    worker.collecting_candles_and_indicators("SOLUSDT", "30")
    worker.collecting_candles_and_indicators("SOLUSDT", "60")
    worker.collecting_candles_and_indicators("SOLUSDT", "240")
    worker.collecting_candles_and_indicators("SOLUSDT", "D")
    worker.collecting_candles_and_indicators("SOLUSDT", "W")
    worker.collecting_levels("SOLUSDT")
