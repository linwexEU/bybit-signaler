from abc import ABC, abstractmethod


class AbstractTelegramClient(ABC): 
    @abstractmethod
    def send_forecast_to_group(self, forecast: str) -> None: ...
