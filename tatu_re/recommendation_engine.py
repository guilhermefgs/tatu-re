import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from tatu_re.utils import send_email
from tatu_re.portfolio import Portfolio
from tatu_re.model import load_model
from tatu_re.model.data_processing.indicators import calculate_features
from typing import Tuple
from datetime import datetime, timedelta

class RecommendationEngine(ABC):

    def __init__(self):
        self.clients = pd.DataFrame([
            {"Nome": "Christian", "Email": "christianleomil@gmail.com"},
            {"Nome": "Gui", "Email": "aateg.german@live.com"}
        ])

    @abstractmethod
    def recommendation(self) -> None:
        pass

    def criteria_for_quantity_of_investment(self, action: str, price: float, portfolio: Portfolio):
        if action == "buy":
            max_quantity_to_buy = portfolio.in_cash // price
            if max_quantity_to_buy == 0:
                action, quantity = "hold", 0 # don't have enough money to execute order
            else:
                action, quantity = "buy", max_quantity_to_buy

        elif action == "sell":
            max_quantity_to_sell = portfolio.n_stocks
            if max_quantity_to_sell == 0:
                action, quantity = "hold", 0  # don't have any stock to share
            else:
                action, quantity = "sell", max_quantity_to_sell

        else:
            action, quantity = "hold", 0  # should do nothing
        
        return action, quantity 

    def send_email(self, action, quantity):
        #send_email(self.clients, action, quantity)
        pass


class Monkey(RecommendationEngine):
    """Monkey gives suggestion for buy, sell or hold
    """

    def recommendation(self, price: float, portfolio: Portfolio) -> Tuple[str, int]:
        """
        If suggestion is buy, Monkey will buy the maximum possible
        If suggestion is sell, Monkey will sell all the portfolio

        This means that when there is no cash, action of buy is equal to hold
        and when there is no assets, action sell is equal to hold

        :param price: current price of the S&P unit share
        :param portfolio: customer portfolio
        :return: quantity of stocks to buy or sell, zero means "do nothing" or "hold"
        """
        u = np.random.uniform(-1, 1)
        action = "buy" if u > 0.3 else ("sell" if u < -0.3 else "hold")

        action, quantity = self.criteria_for_quantity_of_investment(action, price, portfolio)

        self.send_email(action, quantity)

        return action, quantity

class TreeBasedEngine(RecommendationEngine):
    """Recommendation Engine based on Decision Tree model
    """
    model = load_model("decision_tree_v1.sav")

    def recommendation(self, simulation_date: datetime, price: float, portfolio: Portfolio) -> Tuple[str, int]:

        X = calculate_features(simulation_date)
        
        u = self.model.predict(X.iloc[-1].to_frame().T)[0]

        action = "buy" if u > 0.01 else ("sell" if u < -0.01 else "hold")

        action, quantity = self.criteria_for_quantity_of_investment(action, price, portfolio)

        self.send_email(action, quantity)

        return action, quantity
        

