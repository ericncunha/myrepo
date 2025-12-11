from .bybit import BybitAdapter
from .binance import BinanceAdapter


def get_exchange(cfg):
    name = cfg.exchange.lower()
    if name == "bybit":
        if cfg.bybit_api_key is None or cfg.bybit_api_secret is None:
            raise ValueError("Missing ByBit config")
        return BybitAdapter(cfg.bybit_api_key, cfg.bybit_api_secret, cfg.testnet)
    elif name == "binance":
        if cfg.binance_api_key is None or cfg.binance_api_secret is None:
            raise ValueError("Missing Binance config")
        return BinanceAdapter(cfg.binance_api_key, cfg.binance_api_secret, cfg.testnet)
    else:
        raise ValueError(f"Unsupported exchange: {name}")
