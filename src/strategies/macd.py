# src/strategies/macd.py
from strategies.signal import Signal
from indicators import compute_macd_signal

class MACDStrategy:
    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9):
        self.fast = fast
        self.slow = slow
        self.signal = signal

    def evaluate(self, close):
        m = compute_macd_signal(close, fast=self.fast, slow=self.slow, signal=self.signal)
        cross = m["cross"]

        if cross == "bull":
            return Signal("macd", "long", 0.7, m)
        elif cross == "bear":
            return Signal("macd", "short", 0.7, m)
        else:
            return Signal("macd", "flat", 0.0, m)
