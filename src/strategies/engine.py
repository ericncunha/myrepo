# src/strategies/engine.py
from utils import parse_strategy_flags
from strategies.rsi import RSIStrategy
from strategies.macd import MACDStrategy
from strategies.ema_trend import EMATrendStrategy

class StrategyEngine:
    """
    Collects signals from all enabled strategies.
    """
    def __init__(self, strategy_arg: str, rsi_params: dict):
        # user can still do: --strategy rsi,macd,ema
        enabled = parse_strategy_flags(strategy_arg)
        self.enabled = enabled

        self.rsi = RSIStrategy(**rsi_params) if "rsi" in enabled else None
        self.macd = MACDStrategy() if "macd" in enabled else None
        self.ema = EMATrendStrategy() if "ema" in enabled else None

    def evaluate_all(self, close):
        signals = []
        if self.rsi:
            signals.append(self.rsi.evaluate(close))
        if self.macd:
            signals.append(self.macd.evaluate(close))
        if self.ema:
            signals.append(self.ema.evaluate(close))
        return signals
