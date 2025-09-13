from dataclasses import dataclass


@dataclass
class Kline: 
    StartTime: str
    OpenPrice: str
    HighPrice: str
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
            ClosePrice=item[3], Volume=item[4], Turnover=item[5], 
            Timestamp=time, Confirm=True
        )

    @staticmethod
    def build_from_dict(item: dict) -> "Kline": 
        return Kline(
            StartTime=item["start"], OpenPrice=item["open"], HighPrice=item["high"], 
            ClosePrice=item["close"], Volume=item["volume"], Turnover=item["turnover"], 
            Interval=item["interval"], Confirm=item["confirm"], Timestamp=item["timestamp"]
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
