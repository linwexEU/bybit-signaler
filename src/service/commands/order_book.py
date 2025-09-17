from src.infrastructure.bybit import ByBitRESTClient
from src.infrastructure.db.base import session_factory 
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork


class OrderBookCommand: 
    @staticmethod
    def get_and_save_order_book(ticker: str) -> None: 
        # Init ByBitClient
        rest_instance = ByBitRESTClient()

        # Get OrderBook
        order_book = rest_instance.get_order_book(ticker)

        # Save to Db
        with SQLAlchemyUnitOfWork(session_factory) as uow: 
            uow.order_book_repository.insert(order_book.to_dict())
