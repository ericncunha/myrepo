import argparse
from bot import run


def main():
    p = argparse.ArgumentParser(description="traderbot — RSI/MACD Bybit trading bot.")
    p.add_argument("--strategy", required=True, help="Comma-separated strategies (rsi, macd). Example: macd,rsi")
    args = p.parse_args()
    print(f"[INFO] Starting TraderBot with strategy: {args.strategy}")
    run(args.strategy)


if __name__ == "__main__":
    main()