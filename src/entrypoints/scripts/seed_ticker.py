import logging
import random
import sys

from src.infrastructure.bybit.system_manager import SystemManager
from src.service.commands import CandleCommands, IndicatorCommands, OrderBookCommand, LevelCommands
from src.logger import configure_logging, log
from src.config import settings
from src.infrastructure.bybit import ByBitRESTClient

# Configure logging
configure_logging()


@log
def collect_data(ticker: str) -> None: 
    for interval in ["5", "15", "60", "240", "D", "W"]:
        last_candle_id = CandleCommands.get_and_save_candles(ticker, interval)
        IndicatorCommands.get_and_save_indicators(ticker, interval, last_candle_id)
    OrderBookCommand.get_and_save_order_book(ticker)
    LevelCommands.get_and_save_levels(ticker)


@log
def seed_ticker_script(ticker: str) -> None:
    if ticker == "AUTO":
        rest_instance = ByBitRESTClient()
        tickers = random.sample(SystemManager.get_active_tickers(rest_instance.get_tickers(), settings.THRESHOLD), 5)
        tickers = [tk.Symbol for tk in tickers]
        logging.info(f"Auto tickers: {tickers}")

        for tk in tickers:
            collect_data(tk)
    else:
        collect_data(ticker)


if __name__ == "__main__": 
    ticker = sys.argv[1:][0]
    seed_ticker_script(ticker.upper())
