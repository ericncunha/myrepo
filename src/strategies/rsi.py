# src/strategies/rsi.py
from strategies.signal import Signal
from indicators import compute_rsi


class RSIStrategy:
    def __init__(self, period: int, overbought: float, oversold: float, smooth: bool):
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
        self.smooth = smooth

    def evaluate(self, close):
        r = compute_rsi(close, self.period, self.smooth)

        # no data yet
        if r != r:  # NaN check
            return Signal("rsi", "flat", 0.0, {"rsi": r})

        # oversold → long
        if r <= self.oversold:
            # deeper oversold → higher strength
            strength = min(1.0, (self.oversold - r) / 10.0)
            return Signal("rsi", "long", strength, {"rsi": r})

        # overbought → short
        if r >= self.overbought:
            strength = min(1.0, (r - self.overbought) / 10.0)
            return Signal("rsi", "short", strength, {"rsi": r})

        return Signal("rsi", "flat", 0.0, {"rsi": r})
