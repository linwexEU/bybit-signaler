from datetime import datetime, timezone
from typing import Any

from sqlalchemy import TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.base import Base
from src.domain.enums import LevelType


class Candle(Base): 
    __tablename__ = "candles"

    Id: Mapped[int] = mapped_column(primary_key=True, index=True) 
    Ticker: Mapped[str] = mapped_column(nullable=False, index=True) 
    Timeframe: Mapped[str] = mapped_column(nullable=False, index=True) 
    Timestamp: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), index=True)

    Open: Mapped[float] = mapped_column(nullable=False) 
    High: Mapped[float] = mapped_column(nullable=False) 
    Low: Mapped[float] = mapped_column(nullable=False) 
    Close: Mapped[float] = mapped_column(nullable=False)
    Volume: Mapped[float] = mapped_column(nullable=False)

    indicators = relationship("Indicator", back_populates="candle") 


class Indicator(Base): 
    __tablename__ = "indicators"

    Id: Mapped[int] = mapped_column(primary_key=True, index=True)
    CandleId: Mapped[int] = mapped_column(ForeignKey("candles.Id"))

    Timeframe: Mapped[str] = mapped_column(nullable=False, index=True) 

    Ema9: Mapped[float] = mapped_column(nullable=True)
    Ema21: Mapped[float] = mapped_column(nullable=True)
    Rsi: Mapped[float] = mapped_column(nullable=True)

    Macd: Mapped[float] = mapped_column(nullable=True)
    MacdSignal: Mapped[float] = mapped_column(nullable=True) 
    MacdHist: Mapped[float] = mapped_column(nullable=True) 

    BbHigh: Mapped[float] = mapped_column(nullable=True)
    BbLow: Mapped[float] = mapped_column(nullable=True)
    BbMid: Mapped[float] = mapped_column(nullable=True)

    Atr: Mapped[float] = mapped_column(nullable=True)
    Obv: Mapped[float] = mapped_column(nullable=True)

    candle = relationship("Candle", back_populates="indicators")


class OrderBook(Base): 
    __tablename__ = "order_book"

    Id: Mapped[int] = mapped_column(primary_key=True, index=True)
    Ticker: Mapped[str] = mapped_column(nullable=False, index=True)
    Timestamp: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))

    Bids: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    Asks: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)


class Level(Base): 
    __tablename__ = "levels"

    Id: Mapped[int] = mapped_column(primary_key=True, index=True)
    Ticker: Mapped[str] = mapped_column(nullable=False, index=True) 
    LevelPrice: Mapped[float] = mapped_column(nullable=False)
    Strength: Mapped[float] = mapped_column() 
    Type: Mapped[LevelType] = mapped_column(nullable=False)
    LastTouched: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
