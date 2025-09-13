from src.domain.interfaces import AbstractSystemManager


class SystemManager(AbstractSystemManager): 
    @staticmethod
    def get_active_tickers(tickers: list[dict], threshold: int) -> list[dict]:
        return list(
            filter(
                lambda t: float(t["turnover24h"]) > threshold or float(t["volume24h"]) * float(t["lastPrice"]) > threshold, 
                tickers
            )
        )
