from collections import deque

from src.domain.interfaces import AbstractCandleStore 


class CandleStore(AbstractCandleStore):
    def __init__(self): 
        self.candle_queue = deque()

    def push_closed() -> None: 
        pass 

    def  update_partial() -> None: 
        pass 

    def to_dataframe() -> None: 
        pass  
