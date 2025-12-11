from .base import ExchangeAdapter
from binance.client import Client
import pandas as pd


class BinanceAdapter(ExchangeAdapter):
    def __init__(self, api_key, api_secret, testnet=True):
        if testnet:
            self.client = Client(api_key, api_secret, testnet=True)
            self.client.API_URL = "https://testnet.binance.vision/api"
        else:
            self.client = Client(api_key, api_secret)

    def get_klines(self, symbol: str, interval: str, limit=200) -> pd.DataFrame:
        candles = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(candles, columns=[
            "open_time","open","high","low","close","volume",
            "close_time","quote_asset_volume","number_of_trades",
            "taker_buy_base_asset_volume","taker_buy_quote_asset_volume","ignore"
        ])
        df = df.astype({
            "open":"float","high":"float","low":"float",
            "close":"float","volume":"float"
        })
        return df[["open_time","open","high","low","close","volume"]]

    def get_last_price(self, symbol: str) -> float:
        data = self.client.get_symbol_ticker(symbol=symbol)
        return float(data["price"])

    def get_position(self, symbol: str):
        # For Spot: treat holdings as “position”
        info = self.client.get_asset_balance(asset=symbol.replace("USDT",""))
        qty = float(info["free"])
        return {"asset": symbol, "free_qty": qty}

    def place_order(self, symbol: str, side: str, order_type: str, qty: float):
        # Map your generic side/order_type to binance-specific
        if order_type.lower() == "market":
            res = self.client.order_market(symbol=symbol, side=side, quantity=qty)
        else:
            res = self.client.create_order(symbol=symbol, side=side, type=order_type.upper(), quantity=qty)
        print(f"[BINANCE] Order placed: {res}")
        return res

    def set_stop_loss(self, symbol: str, stop_price: float):
        # Spot: use STOP_LOSS or OCO order
        res = self.client.create_order(
            symbol=symbol,
            side="SELL",
            type="STOP_LOSS",
            stopPrice=stop_price,
            quantity=1  # Example; you'll tie to actual qty
        )
        print(f"[BINANCE] Stop-loss set: {res}")
        return res

    def set_take_profit(self, symbol: str, take_price: float, side: str, qty: float):
        # Spot: use OCO or TAKE_PROFIT market
        res = self.client.create_order(
            symbol=symbol,
            side=side,
            type="TAKE_PROFIT_MARKET",
            stopPrice=take_price,
            closePosition=True  # if using futures
        )
        print(f"[BINANCE] Take-profit set: {res}")
        return res
