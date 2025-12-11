from .base import ExchangeAdapter
from pybit.unified_trading import HTTP
import pandas as pd


class BybitAdapter(ExchangeAdapter):
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = HTTP(api_key=api_key, api_secret=api_secret, testnet=testnet)

    def get_klines(self, symbol, interval, limit=200):
        res = self.client.get_kline(category="linear", symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(res["result"]["list"]).astype(float)
        df.columns = ["timestamp", "open", "high", "low", "close", "volume"]
        return df

    def get_last_price(self, symbol):
        res = self.client.get_tickers(category="linear", symbol=symbol)
        return float(res["result"]["list"][0]["lastPrice"])

    def get_position(self, symbol):
        res = self.client.get_positions(category="linear", symbol=symbol)
        return res["result"]["list"][0]

    def place_order(self, symbol, side, order_type, qty):
        res = self.client.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType=order_type,
            qty=qty,
            timeInForce="GoodTillCancel"
        )
        print(f"[BYBIT] Order placed: {res}")
        return res

    def set_stop_loss(self, symbol, stop_price):
        return self.client.set_trading_stop(
            category="linear", symbol=symbol, stopLoss=stop_price, slTriggerB="LastPrice"
        )

    def set_take_profit(self, symbol, take_price, side, qty):
        return self.client.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Limit",
            reduceOnly=True,
            qty=qty,
            price=take_price,
        )
