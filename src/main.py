import schedule

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
        self.worker = ForecastWorker() 
        self.tg_client = TgClient()

    def schedule_tasks(self) -> None: 
        for ticker in self.tickers:
            schedule.every(5).minutes.do(collecting_data_every_5m, ticker=ticker.Symbol)
            schedule.every(15).minutes.do(collecting_data_every_15m, ticker=ticker.Symbol)
            schedule.every(1).hour.do(collecting_data_every_1h, ticker=ticker.Symbol)
            schedule.every(1).hour.do(collecting_order_book_every_1h, ticker=ticker.Symbol)
            schedule.every(1).hour.do(collecting_levels_every_1h, ticker=ticker.Symbol)
            schedule.every(4).hours.do(collecting_data_every_4h, ticker=ticker.Symbol)
            schedule.every(5).hours.do(forecast_task, ticker=ticker.Symbol, worker=self.worker, telegram_client=self.tg_client)
            schedule.every().day.at("00:00").do(collecting_data_every_day, ticker=ticker.Symbol)
            schedule.every().monday.do(collecting_data_every_week, ticker=ticker.Symbol)
        

if __name__ == "__main__": 
    bbbs = BybitBotSignaler()
    bbbs.schedule_tasks()

    while True: 
        schedule.run_pending()
