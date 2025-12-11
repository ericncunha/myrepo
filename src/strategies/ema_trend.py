from strategies.signal import Signal
from indicators import compute_ema


class EMATrendStrategy:
    """
    Trend-following strategy based on the relationship between
    fast and slow Exponential Moving Averages (EMA).
    """

    def __init__(self, fast: int = 9, slow: int = 21):
        self.fast = fast
        self.slow = slow

    def evaluate(self, close):
        """
        Evaluate trend direction:
        - long when EMA fast > EMA slow
        - short when EMA fast < EMA slow
        - flat otherwise
        """
        ema = compute_ema(close, self.fast, self.slow)
        ema_fast = ema["ema_fast"]
        ema_slow = ema["ema_slow"]

        # Handle NaN (not enough data)
        if not all(map(lambda x: x == x, [ema_fast, ema_slow])):
            return Signal("ema_trend", "flat", 0.0, ema)

        if ema_fast > ema_slow:
            return Signal("ema_trend", "long", 0.5, ema)
        elif ema_fast < ema_slow:
            return Signal("ema_trend", "short", 0.5, ema)
        else:
            return Signal("ema_trend", "flat", 0.0, ema)
