import numpy as np
from typing import Tuple

class Portfolio:
    
    def __init__(self, total=0, n_stocks=0, unit_price=0):
        """
        total: Total in cash + stock value
        n_stocks: number of stocks in portfolio
        in_cash: cash in portfolio
        unit_price: (current) price of stock unit
        timeseries: timeseries of portfolio performance over days
        """

        # TODO buy units
        self.total = total
        self.n_stocks = n_stocks
        self.unit_price = unit_price
        self.in_cash = self.total - self.n_stocks*self.unit_price
        self.timeseries = [] # TODO make this an actual timeseries

    def buy(self, n_units):
        self.in_cash -= n_units*self.unit_price
        self.n_stocks += n_units

    def sell(self, n_units):
        self.buy(-n_units)

    def update_price(self, new_price):
        self.unit_price = new_price
        self.total = self.in_cash + self.n_stocks*self.unit_price

    def append_day(self):
        self.timeseries.append(self.total)

    def decicion(self, x=None, model=None) -> Tuple[str, np.float64]:
        """Function that returns the recommended action (buy/sell/hold, amount) 
        given the model inputs and the model itself

        :param x: input of the model - time series data
        :param model: model object
        """

        
        # TODO read model and do prediction = model.predict(x)
        # TODO Strategy can be a class
        in_asset = self.n_stocks*self.unit_price # or total - cash?
        total = self.total
        amount = 0
        prediction = np.random.uniform(-1, 1)
        label = "buy" if prediction > 0.3 else ("sell" if prediction < -0.3 else "hold")

        if label == "sell":
            label, amount = label, -min(abs(prediction)*total, in_asset)
        elif label == "buy":
            label, amount = label, min(abs(prediction)*total, total-in_asset) 


        n_units = amount // self.unit_price
        self.buy(n_units)
        return label, amount
