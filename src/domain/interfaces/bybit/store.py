from abc import ABC, abstractmethod


class AbstractCandleStore(ABC): 
    @abstractmethod
    def push_closed() -> None: ...

    @abstractmethod 
    def update_partial() -> None: ...

    @abstractmethod 
    def to_dataframe() -> None: ...
