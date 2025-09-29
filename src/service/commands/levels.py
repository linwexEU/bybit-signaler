from src.domain.models import OrderBook, Level
from src.domain.enums import LevelType
from src.infrastructure.db.base import session_factory 
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from src.logger import log


class LevelCommands: 
    @staticmethod
    @log
    def get_and_save_levels(ticker: str) -> None: 
        with SQLAlchemyUnitOfWork(session_factory) as uow: 
            order_book = uow.order_book_repository.filters({"Ticker": ticker})[0]
            order_book: OrderBook = OrderBook.from_orm(order_book)
            
            # Top 10 bid
            for bid in order_book.Bids[:10]:
                support_level = Level(
                    Ticker=order_book.Ticker, LevelPrice=float(bid.BidPrice), Strength=float(bid.BidSize), 
                    Type=LevelType.Support, LastTouched=order_book.Timestamp
                )
                uow.level_repository.insert(support_level.to_dict())

            # Top 10 ask
            for ask in order_book.Asks[:10]: 
                resistance_level = Level(
                    Ticker=order_book.Ticker, LevelPrice=float(ask.AskPrice), Strength=float(ask.AskSize), 
                    Type=LevelType.Resistance, LastTouched=order_book.Timestamp
                )
                uow.level_repository.insert(resistance_level.to_dict())
