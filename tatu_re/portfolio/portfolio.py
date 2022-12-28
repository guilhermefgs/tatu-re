import numpy as np

from datetime import datetime
from typing import List

class Portfolio:

    def __init__(self, initial_capital, start_date) -> None:

        # static variable
        self.initial_capital: float = initial_capital
        self.start_date: datetime = start_date

        # dynamic variables
        self.in_cash: float = self.initial_capital
        self.in_asset: float = 0
        self.n_stocks: int = 0

        # timeseries
        self.operations: List = []
        self.in_cash_series: List = []
        self.in_asset_series: List = []

    def update(self, date, price, quantity, action) -> None:
        self.operations.append(
            {
                "date": date,
                "price": price,
                "quantity": quantity,
                "action": action
            }
        )
        amount = price * quantity
        if action == "buy":
            self.in_cash -= amount
            self.n_stocks += quantity
        elif action == "sell":
            self.in_cash += amount
            self.n_stocks -= quantity
        self.in_asset = self.n_stocks * price
        self.in_cash_series.append(self.in_cash)
        self.in_asset_series.append(self.in_asset)

    def cumprod_returns(self):
        total = np.add(self.in_cash_series, self.in_asset_series)
        return (total.pct_change() + 1).cumprod()

