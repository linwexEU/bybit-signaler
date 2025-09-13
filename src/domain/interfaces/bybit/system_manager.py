from abc import ABC, abstractmethod


class AbstractSystemManager(ABC):
    @staticmethod
    @abstractmethod
    def get_active_tickers(tickers: list[dict], threshold: int) -> list[dict]: ...
