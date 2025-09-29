import logging
import sys

import schedule

from src.logger import configure_logging
from src.infrastructure.telegram import TgClient
from src.entrypoints.workers.worker import ForecastWorker
from src.infrastructure.schedule.tasks import collecting_data_every_15m, collecting_data_every_1h, collecting_data_every_4h, \
                                              collecting_data_every_5m, collecting_data_every_day, collecting_data_every_week, \
                                              forecast_task, collecting_order_book_every_1h, collecting_levels_every_1h
from src.infrastructure.bybit import ByBitRESTClient, SystemManager
from src.config import settings


class BybitBotSignaler:
    def __init__(self) -> None: 
        self.rest_instance = ByBitRESTClient() 

        self.tickers = SystemManager.get_active_tickers(self.rest_instance.get_tickers(), settings.THRESHOLD)[:5]
        self.tickers = [tk.Symbol for tk in self.tickers]

        self.worker = ForecastWorker() 
        self.tg_client = TgClient()

    def schedule_tasks(self, tickers: list[str] | None = None) -> None:
        self.tickers = tickers if tickers else self.tickers

        # Schedule collecting data
        for ticker in self.tickers:
            schedule.every(5).minutes.do(collecting_data_every_5m, ticker=ticker)
            schedule.every(15).minutes.do(collecting_data_every_15m, ticker=ticker)
            schedule.every(1).hour.do(collecting_data_every_1h, ticker=ticker)
            schedule.every(1).hour.do(collecting_order_book_every_1h, ticker=ticker)
            schedule.every(1).hour.do(collecting_levels_every_1h, ticker=ticker)
            schedule.every(4).hours.do(collecting_data_every_4h, ticker=ticker)
            schedule.every().day.at("00:00").do(collecting_data_every_day, ticker=ticker)
            schedule.every().monday.do(collecting_data_every_week, ticker=ticker)
           
        logging.info("Setup all collecting schedule tasks")

        # Schedule forecasting
        for minute, ticker in enumerate(self.tickers, start=1):
            schedule.every(5).hours.at(f"00:{minute:02d}").do(
                forecast_task, ticker=ticker, worker=self.worker, telegram_client=self.tg_client
            )
        
        logging.info("Setup all forecasting schedule tasks")


def run_scheduling(tickers: list[str] | None = None) -> None: 
    # Init BybitBotSignaler
    bbbs = BybitBotSignaler()
    bbbs.schedule_tasks(tickers)

    # Run scheduling
    logging.info("Start scheduling...")
    try:
        while True: 
            schedule.run_pending()
    except KeyboardInterrupt: 
        logging.info("End scheduling")
            

if __name__ == "__main__":
    # Configure logging
    configure_logging() 

    # Run scheduling
    try:
        tickers = [sys.argv[1:][0], sys.argv[1:][1], sys.argv[1:][2], sys.argv[1:][3], sys.argv[1:][4]]
    except: 
        tickers = None
    run_scheduling(tickers)
