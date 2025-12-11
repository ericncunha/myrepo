import math
from decimal import Decimal, ROUND_FLOOR


def round_to_tick(price: float, tick_size: float) -> float:
    if tick_size <= 0:
        return price
    return float((Decimal(str(price)) / Decimal(str(tick_size))).quantize(Decimal("1"), rounding=ROUND_FLOOR)
                 * Decimal(str(tick_size)))


def round_to_step(qty: float, qty_step: float) -> float:
    if qty_step <= 0:
        return qty
    return math.floor(qty / qty_step) * qty_step


def safe_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default


def parse_strategy_flags(arg: str) -> list[str]:
    """Accept comma-separated list (e.g., 'macd,rsi,ema')."""
    if not arg or not arg.strip():
        raise ValueError("No trading strategy selected. Use one or more of: rsi, macd, ema")

    parts = [p.strip().lower() for p in arg.split(",") if p.strip()]
    valid = {"rsi", "macd", "ema"}
    order = []
    for p in parts:
        if p not in valid:
            raise ValueError(f"Unknown strategy '{p}'. Valid: rsi, macd, ema")
        if p not in order:
            order.append(p)
    return order

