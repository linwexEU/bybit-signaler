from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone

from src.domain.enums import LevelType
from src.infrastructure.db.models import Candle as DbCandle
from src.infrastructure.db.models import Indicator as DbIndicator
from src.infrastructure.db.models import OrderBook as DbOrderBook
from src.infrastructure.db.models import Level as DbLevel


@dataclass
class Kline: 
    StartTime: str
    OpenPrice: str
    HighPrice: str
    LowPrice: str
    ClosePrice: str
    Volume: str
    Turnover: str
    Interval: int | None = None
    Confirm: bool | None = None
    Timestamp: int | None = None

    @staticmethod
    def build_obj(item: list, time: int) -> "Kline": 
        return Kline(
            StartTime=item[0], OpenPrice=item[1], HighPrice=item[2], 
            LowPrice=item[3], ClosePrice=item[4], Volume=item[5],
            Turnover=item[6], Timestamp=time, Confirm=True
        )

    @staticmethod
    def build_from_dict(item: dict) -> "Kline": 
        return Kline(
            StartTime=item["start"], OpenPrice=item["open"], HighPrice=item["high"], 
            ClosePrice=item["close"], Volume=item["volume"], Turnover=item["turnover"], 
            Interval=item["interval"], Confirm=item["confirm"], Timestamp=item["timestamp"],
            LowPrice=item["low"]
        )


@dataclass
class Ticker: 
    Symbol: str | None
    Bid1Price: str | None
    Bid1Size: str | None
    Ask1Price: str | None
    Ask1Size: str | None
    LastPrice: str | None
    PrevPrice24h: str | None
    Price24hPcnt: str | None
    HighPrice24h: str | None
    LowPrice24h: str | None
    Turnover24h: str | None
    Volume24h: str | None
    UsdIndexPrice: str | None

    @staticmethod 
    def build_obj(item: dict) -> "Ticker": 
        return Ticker(
            Symbol=item.get("symbol"), Bid1Price=item.get("bid1Price"), Bid1Size=item.get("bid1Size"), 
            Ask1Price=item.get("ask1Price"), Ask1Size=item.get("ssk1Size"), LastPrice=item.get("lastPrice"),
            PrevPrice24h=item.get("prevPrice24h"), Price24hPcnt=item.get("price24hPcnt"), HighPrice24h=item.get("highPrice24h"), 
            LowPrice24h=item.get("lowPrice24h"), Turnover24h=item.get("turnover24h"), Volume24h=item.get("volume24h"), 
            UsdIndexPrice=item.get("usdIndexPrice")
        )


@dataclass
class Bid: 
    BidPrice: str
    BidSize: str

    @staticmethod
    def build_obj(item: list) -> "Bid": 
        return Bid(BidPrice=item[0], BidSize=item[1])


@dataclass
class Ask: 
    AskPrice: str
    AskSize: str 

    @staticmethod
    def build_obj(item: list) -> "Ask": 
        return Ask(AskPrice=item[0], AskSize=item[1])


@dataclass
class EntityToDict:

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class OrderBook(EntityToDict):
    Ticker: str
    Timestamp: datetime = field(default=datetime.now(timezone.utc), kw_only=True) 
    Bids: list[Bid]
    Asks: list[Ask]
    
    @staticmethod
    def build_obj(ticker: str, order_book: dict) -> "OrderBook":
        bids = [Bid.build_obj(bid) for bid in order_book["b"]]
        asks = [Ask.build_obj(ask) for ask in order_book["a"]] 
        return OrderBook(Ticker=ticker, Bids=bids, Asks=asks)
    
    @staticmethod 
    def from_orm(order_book: DbOrderBook) -> "OrderBook": 
        bids = [Bid(BidPrice=item["BidPrice"], BidSize=item["BidSize"]) for item in order_book.Bids]
        asks = [Ask(AskPrice=item["AskPrice"], AskSize=item["AskPrice"]) for item in order_book.Asks]
        return OrderBook(Ticker=order_book.Ticker, Timestamp=order_book.Timestamp, Bids=bids, Asks=asks)


@dataclass
class Candle:
    Id: int | None = field(default=None, kw_only=True)
    Ticker: str
    Timeframe: str
    Timestamp: datetime
    Open: float
    High: float
    Low: float
    Close: float
    Volume: float

    @staticmethod
    def from_orm(candle: DbCandle) -> "Candle": 
        return Candle(
            Ticker=candle.Ticker, Timeframe=candle.Timeframe, Timestamp=candle.Timestamp, Id=candle.Id,
            Open=candle.Open, High=candle.High, Low=candle.Low, Close=candle.Close, Volume=candle.Volume
        )
    
    def to_dict(self) -> dict: 
        return {
            "Ticker": self.Ticker, "Timeframe": self.Timeframe, "Timestamp": self.Timestamp, "Open": self.Open, 
            "High": self.High, "Low": self.Low, "Close": self.Close, "Volume": self.Volume
        }


@dataclass
class Indicator(EntityToDict):
    CandleId: int
    Timeframe: str
    Ema9: float
    Ema21: float
    Rsi: float
    Macd: float
    MacdSignal: float
    MacdHist: float
    BbHigh: float
    BbLow: float
    BbMid: float
    Atr: float
    Obv: float

    @staticmethod
    def from_orm(indicator: DbIndicator) -> list["Indicator"]: 
        return Indicator(
            CandleId=indicator.CandleId, Ema9=indicator.Ema9, Ema21=indicator.Ema21, Rsi=indicator.Rsi,
            Macd=indicator.Macd, MacdSignal=indicator.MacdSignal, MacdHist=indicator.MacdHist, Obv=indicator.Obv,
            BbHigh=indicator.BbHigh, BbLow=indicator.BbLow, BbMid=indicator.BbMid, Atr=indicator.Atr, Timeframe=indicator.Timeframe
        )


@dataclass
class Level(EntityToDict):
    Ticker: str
    LevelPrice: float
    Strength: int
    Type: LevelType
    LastTouched: datetime

    @staticmethod
    def from_orm(level: DbLevel) -> "Level": 
        return Level(
            Ticker=level.Ticker, LevelPrice=level.LevelPrice, Strength=level.Strength, 
            Type=level.Type, LastTouched=level.LastTouched
        )
