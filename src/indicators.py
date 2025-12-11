import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD


def compute_rsi(close: pd.Series, period: int, smooth: bool = False) -> float:
    """
    Compute the RSI for a given closing price series.
    Optionally apply a moving average to smooth the RSI curve.
    """
    if len(close) < period + 2:
        return float("nan")

    rsi = RSIIndicator(close=close, window=period).rsi()

    if smooth:
        rsi = rsi.rolling(window=period).mean()

    return float(rsi.iloc[-1])


def compute_macd_signal(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> dict:
    """
    Compute MACD, signal line, histogram, and detect bullish/bearish crossover.
    Returns a dict with current MACD values and crossover direction.
    """
    if len(close) < slow + signal + 5:
        return {"macd": 0.0, "signal": 0.0, "hist": 0.0, "cross": None}

    m = MACD(close=close, window_slow=slow, window_fast=fast, window_sign=signal)
    macd = m.macd()
    sig = m.macd_signal()
    hist = macd - sig

    prev = hist.iloc[-2]
    curr = hist.iloc[-1]

    # Detect crossovers
    cross = None
    if prev <= 0 < curr:
        cross = "bull"
    elif prev >= 0 > curr:
        cross = "bear"

    return {
        "macd": float(macd.iloc[-1]),
        "signal": float(sig.iloc[-1]),
        "hist": float(hist.iloc[-1]),
        "cross": cross,
    }


def compute_ema(close: pd.Series, fast: int = 9, slow: int = 21) -> dict:
    """
    Compute fast and slow Exponential Moving Averages (EMA).
    Returns both as floats in a dict.
    """
    if len(close) < slow + 2:
        return {"ema_fast": float("nan"), "ema_slow": float("nan")}

    ema_fast = close.ewm(span=fast, adjust=False).mean().iloc[-1]
    ema_slow = close.ewm(span=slow, adjust=False).mean().iloc[-1]

    return {
        "ema_fast": float(ema_fast),
        "ema_slow": float(ema_slow),
    }


# TODO: ADD strategy
def compute_atr(df: pd.DataFrame, period: int = 14) -> float:
    """
    Compute the Average True Range (ATR) for volatility filtering.
    ATR helps to avoid trading in low-volatility periods.
    """
    if not {"high", "low", "close"}.issubset(df.columns):
        return float("nan")

    high = df["high"]
    low = df["low"]
    close = df["close"]

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = tr.rolling(window=period).mean()
    return float(atr.iloc[-1])
