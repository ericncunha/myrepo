from strategies.signal import Signal


class SignalCombiner:
    def __init__(self, min_total_strength: float = 1.0):
        self.min_total_strength = min_total_strength

    def decide(self, signals: list[Signal]) -> str | None:
        long_score = 0.0
        short_score = 0.0

        for s in signals:
            if s.direction == "long":
                long_score += s.strength
            elif s.direction == "short":
                short_score += s.strength

        # simple majority + threshold
        if long_score >= self.min_total_strength and long_score > short_score:
            return "long"
        if short_score >= self.min_total_strength and short_score > long_score:
            return "short"
        return None
