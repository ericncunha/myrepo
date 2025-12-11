from dataclasses import dataclass


@dataclass
class Signal:
    name: str          # e.g. "rsi", "macd", "ema_trend"
    direction: str     # "long" | "short" | "flat"
    strength: float    # 0.0 - 1.0
    meta: dict         # extra info (rsi value, macd cross, etc.)
