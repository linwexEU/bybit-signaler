from abc import ABC, abstractmethod


class AbstractTradingView(ABC): 
    @abstractmethod
    def login_without_automation(self, time_to_wait: int = 120) -> None: ...

    @abstractmethod
    def get_ticker_chart(self, ticker: str) -> None: ...

    @abstractmethod 
    def close_driver(self) -> None: ...

    @abstractmethod 
    def _save_login_cookies(self) -> None: ...

    @abstractmethod 
    def _load_login_cookies(self) -> None: ...

    @abstractmethod 
    def _wait_until_page_loaded(self) -> None: ...

    @abstractmethod 
    def _wait_for_element(self, element: tuple) -> None: ... 
