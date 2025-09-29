from src.infrastructure.telegram.client import TgClient
from src.service.commands import CandleCommands, IndicatorCommands, OrderBookCommand, LevelCommands
from src.entrypoints.workers.worker import ForecastWorker
from src.logger import log


@log
def collecting_data_every_5m(ticker: str) -> None: 
    candle_id = CandleCommands.get_and_save_candles(ticker) 
    IndicatorCommands.get_and_save_indicators(ticker, "5", candle_id)


@log
def collecting_data_every_15m(ticker: str) -> None:
    candle_id = CandleCommands.get_and_save_candles( ticker, interval="15")
    IndicatorCommands.get_and_save_indicators(ticker, "15", candle_id)


@log
def collecting_data_every_1h(ticker: str) -> None:
    candle_id = CandleCommands.get_and_save_candles(ticker, interval="60") 
    IndicatorCommands.get_and_save_indicators(ticker, "60", candle_id) 


@log
def collecting_data_every_4h(ticker: str) -> None: 
    candle_id = CandleCommands.get_and_save_candles(ticker, interval="240")
    IndicatorCommands.get_and_save_indicators(ticker, "240", candle_id)


@log
def collecting_data_every_day(ticker: str) -> None: 
    candle_id = CandleCommands.get_and_save_candles(ticker, interval="D")
    IndicatorCommands.get_and_save_indicators(ticker, "D", candle_id)


@log
def collecting_data_every_week(ticker: str) -> None:
    candle_id = CandleCommands.get_and_save_candles(ticker, interval="W")
    IndicatorCommands.get_and_save_indicators(ticker, "W", candle_id)


@log
def collecting_order_book_every_1h(ticker: str) -> None: 
    OrderBookCommand.get_and_save_order_book(ticker)


@log
def collecting_levels_every_1h(ticker: str) -> None: 
    LevelCommands.get_and_save_levels(ticker)


@log
def forecast_task(ticker: str, worker: ForecastWorker, telegram_client: TgClient) -> str: 
    forecast = worker.make_a_forecast(ticker)
    telegram_client.send_forecast_to_group(forecast)
