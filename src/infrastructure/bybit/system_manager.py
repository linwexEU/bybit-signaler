import pandas
import ta

from src.domain.interfaces import AbstractSystemManager
from src.domain.models import Indicator, Ticker
from src.infrastructure.redis import RedisClient
from src.logger import log


class SystemManager(AbstractSystemManager): 
    @staticmethod
    @log
    def get_active_tickers(tickers: list[Ticker], threshold: int) -> list[Ticker]:
        return list(
            filter(
                lambda t: float(t.Turnover24h) > threshold or float(t.Volume24h) * float(t.LastPrice) > threshold, 
                tickers
            )
        )

    @staticmethod
    @log
    def calculate_indicators(dataframe: pandas.DataFrame, interval: str, candle_id: int) -> Indicator:
        if dataframe.empty or len(dataframe) < 21:
            raise ValueError("Too small dataframe. Can't do calculation")

        # EMA
        ema9 = ta.trend.EMAIndicator(close=dataframe['close'], window=9).ema_indicator()
        ema21 = ta.trend.EMAIndicator(close=dataframe['close'], window=21).ema_indicator()

        # RSI
        rsi = ta.momentum.RSIIndicator(close=dataframe['close'], window=14).rsi()

        # MACD
        macd_indicator = ta.trend.MACD(close=dataframe['close'])
        macd = macd_indicator.macd()
        macd_signal = macd_indicator.macd_signal()
        macd_hist = macd_indicator.macd_diff()

        # Bollinger Bands
        bbands = ta.volatility.BollingerBands(close=dataframe['close'], window=20, window_dev=2)
        bb_high = bbands.bollinger_hband()
        bb_low = bbands.bollinger_lband()
        bb_mid = bbands.bollinger_mavg()

        # ATR
        atr = ta.volatility.AverageTrueRange(high=dataframe['high'], low=dataframe['low'],
                                             close=dataframe['close'], window=14).average_true_range()

        # OBV
        obv = ta.volume.OnBalanceVolumeIndicator(close=dataframe['close'],
                                                 volume=dataframe['volume']).on_balance_volume()

        return Indicator(CandleId=candle_id, Ema9=float(ema9.iloc[-1]), Ema21=float(ema21.iloc[-1]), Rsi=float(rsi.iloc[-1]),
                         Macd=float(macd.iloc[-1]), MacdSignal=float(macd_signal.iloc[-1]), MacdHist=float(macd_hist.iloc[-1]),
                         BbHigh=float(bb_high.iloc[-1]), BbLow=float(bb_low.iloc[-1]), BbMid=float(bb_mid.iloc[-1]),
                         Atr=float(atr.iloc[-1]), Obv=float(obv.iloc[-1]), Timeframe=interval)

    @staticmethod
    @log
    def to_dataframe(ticker: str) -> pandas.DataFrame:
        klines = None 
        with RedisClient() as redis_client: 
            klines = redis_client.get(ticker)

        if not klines:
            return pandas.DataFrame()

        data = [
            {
                "timestamp": int(k["Timestamp"]) if k["Timestamp"] else None,
                "start_time": k["StartTime"],
                "open": float(k["OpenPrice"]),
                "high": float(k["HighPrice"]),
                "low": float(k["LowPrice"]),
                "close": float(k["ClosePrice"]),
                "volume": float(k["Volume"]),
                "turnover": float(k["Turnover"]),
                "interval": k["Interval"],
                "confirm": k["Confirm"]
            }
            for k in klines
        ]

        dataframe = pandas.DataFrame(data)

        # Sort by time
        dataframe = dataframe.sort_values("timestamp").reset_index(drop=True)
        return dataframe
