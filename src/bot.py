# src/bot.py
import time
from config import Settings
from exchange.factory import get_exchange
from strategies.engine import StrategyEngine
from strategies.combiner import SignalCombiner

def run(strategy_arg: str):
    cfg = Settings.load()
    exchange = get_exchange(cfg)

    print(f"[INFO] Using {cfg.exchange.upper()} exchange")
    print(f"[INFO] Trading {cfg.symbol} | Strategies: {strategy_arg}")

    engine = StrategyEngine(strategy_arg, {
        "period": cfg.rsi_period,
        "overbought": cfg.rsi_overbought,
        "oversold": cfg.rsi_oversold,
        "smooth": cfg.smooth_rsi,
    })
    combiner = SignalCombiner(min_total_strength=1.0)

    print(f"[INFO] Active strategies: {engine.enabled}")

    while True:
        try:
            # 1) check open position (only if your exchange supports it)
            position = exchange.get_position(cfg.symbol)
            # HERE: your binance spot adapter may return {}, so guard it
            size = float(position.get("size", 0)) if position else 0.0

            if size > 0:
                side = position.get("side", "").lower()
                entry = float(position.get("entry_price", 0))
                print(f"[INFO] Open position {side} {size} @ {entry}")

                tp_pct = cfg.tp_pct
                sl_pct = cfg.sl_pct

                if side == "buy":
                    tp_price = entry * (1 + tp_pct / 100)
                    sl_price = entry * (1 - sl_pct / 100)
                    tp_side = "Sell"
                else:
                    tp_price = entry * (1 - tp_pct / 100)
                    sl_price = entry * (1 + sl_pct / 100)
                    tp_side = "Buy"

                try:
                    exchange.set_take_profit(cfg.symbol, tp_price, tp_side, size)
                    exchange.set_stop_loss(cfg.symbol, sl_price)
                    print(f"[INFO] TP/SL attached (TP={tp_price:.2f}, SL={sl_price:.2f})")
                except Exception as inner:
                    print(f"[WARN] Could not set TP/SL on this exchange: {inner}")

                time.sleep(10)
                continue

            # 2) get candles
            df = exchange.get_klines(cfg.symbol, cfg.timeframe)
            close_series = df["close"]

            # 3) get all signals
            signals = engine.evaluate_all(close_series)
            # debug
            print(" | ".join(f"{s.name}:{s.direction}:{s.strength:.2f}" for s in signals))

            # 4) combine
            decision = combiner.decide(signals)
            if not decision:
                print("[WAIT] No consensus — waiting...")
                time.sleep(5)
                continue

            # 5) size
            last_price = exchange.get_last_price(cfg.symbol)
            qty = cfg.usdt / last_price
            print(f"[TRADE] Decision = {decision.upper()} | Price = {last_price:.2f} | Qty = {qty:.6f}")

            # 6) place order
            if decision == "long":
                exchange.place_order(cfg.symbol, "BUY", "MARKET", qty)
            else:
                exchange.place_order(cfg.symbol, "SELL", "MARKET", qty)

            time.sleep(5)

        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(10)
