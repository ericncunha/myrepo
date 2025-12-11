from abc import ABC, abstractmethod
import pandas as pd


class ExchangeAdapter(ABC):
    """Abstract base class for all exchange connectors."""

    @abstractmethod
    def get_klines(self, symbol: str, interval: str, limit: int = 200) -> pd.DataFrame:
        """Return OHLCV data as a pandas DataFrame."""
        pass

    @abstractmethod
    def get_last_price(self, symbol: str) -> float:
        """Return latest market price."""
        pass

    @abstractmethod
    def get_position(self, symbol: str):
        """Return open position details if any."""
        pass

    @abstractmethod
    def place_order(self, symbol: str, side: str, order_type: str, qty: float):
        """Place a buy/sell order."""
        pass

    @abstractmethod
    def set_stop_loss(self, symbol: str, stop_price: float):
        """Set stop loss for active position."""
        pass

    @abstractmethod
    def set_take_profit(self, symbol: str, take_price: float, side: str, qty: float):
        """Set take profit order."""
        pass
