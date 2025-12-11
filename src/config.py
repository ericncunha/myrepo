import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


def _env_str(key, default=""):
    return os.getenv(key, default)


def _env_float(key, default):
    try:
        return float(os.getenv(key, default))
    except Exception:
        return float(default)


def _env_int(key, default):
    try:
        return int(os.getenv(key, default))
    except Exception:
        return int(default)


def _env_bool(key, default=False):
    val = os.getenv(key)
    if val is None:
        return default
    return str(val).lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    exchange: str
    binance_api_key: str | None
    binance_api_secret: str | None
    bybit_api_key: str | None
    bybit_api_secret: str | None
    symbol: str
    timeframe: str
    usdt: float
    tp_pct: float
    sl_pct: float
    rsi_period: int
    rsi_overbought: float
    rsi_oversold: float
    smooth_rsi: bool
    testnet: bool

    @staticmethod
    def load() -> "Settings":
        return Settings(
            exchange=os.getenv("EXCHANGE", "binance"),
            binance_api_key=os.getenv("BINANCE_API_KEY"),
            binance_api_secret=os.getenv("BYBIT_API_SECRET"),
            bybit_api_key=_env_str("BYBIT_API_KEY"),
            bybit_api_secret=_env_str("BYBIT_API_SECRET"),
            symbol=_env_str("SYMBOL", "BTCUSDT"),
            timeframe=_env_str("TIMEFRAME", "5"),
            usdt=_env_float("USDT", 10),
            tp_pct=_env_float("TP_PCT", 0.2),
            sl_pct=_env_float("SL_PCT", 0.4),
            rsi_period=_env_int("RSI_PERIOD", 14),
            rsi_overbought=_env_float("RSI_OVERBOUGHT", 70),
            rsi_oversold=_env_float("RSI_OVERSOLD", 30),
            smooth_rsi=_env_bool("SMOOTH_RSI", False),
            testnet=_env_bool("TESTNET", False),
        )
