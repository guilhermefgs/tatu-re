import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from tatu_re.utils import send_email
from tatu_re.portfolio import Portfolio
from typing import Tuple
import random as rd

class RecommendationEngine(ABC):

    def __init__(self):
        self.clients = pd.DataFrame([
            {"Nome": "Christian", "Email": "christianleomil@gmail.com"},
            {"Nome": "Gui", "Email": "aateg.german@live.com"}
        ])

    @abstractmethod
    def recommendation(self):
        pass


class Monkey(RecommendationEngine):
    """Monkey gives suggestion for buy, sell or hold
    """

    def recommendation(self, price, portfolio: Portfolio) -> Tuple[str, int]:
        """
        If suggestion is buy, Monkey will buy the maximum possible
        If suggestion is sell, Monkey will sell all the portfolio

        This means that when there is no cash, action of buy is equal to hold
        and when there is no assets, action sell is equal to hold

        :param price: current price of the S&P unit share
        :param portfolio: customer portfolio
        :return: quantity of stocks to buy or sell, zero means "do nothing" or "hold"
        """
        u = np.random.uniform(-1, 1.0)
        action = "buy" if u > 1/3 else ("sell" if u < -1/3 else "hold")

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

        #send_email(self.clients, action, quantity)
        return action, quantity
    
class MonkeyEvolution(RecommendationEngine):
    """Monkey gives suggestion for buy, sell or hold, and also random quantities
    """
    
    def recommendation(self, price, portfolio: Portfolio) -> Tuple[str, int]:
        """
        If suggestion is buy, Monkey will buy the maximum possible
        If suggestion is sell, Monkey will sell all the portfolio

        This means that when there is no cash, action of buy is equal to hold
        and when there is no assets, action sell is equal to hold

        :param price: current price of the S&P unit share
        :param portfolio: customer portfolio
        :return: quantity of stocks to buy or sell, zero means "do nothing" or "hold"
        """
        u = np.random.uniform(-1, 1.0)
        action = "buy" if u > 1/3 else ("sell" if u < -1/3 else "hold")

        if action == "buy":
            max_quantity_to_buy = (portfolio.in_cash*rd.uniform(0,1))//price
            if max_quantity_to_buy == 0:
                action, quantity = "hold", 0 # don't have enough money to execute order
            else:
                action, quantity = "buy", max_quantity_to_buy

        elif action == "sell":
            max_quantity_to_sell = int(portfolio.n_stocks*rd.uniform(0,1))
            if max_quantity_to_sell == 0:
                action, quantity = "hold", 0  # don't have any stock to share
            else:
                action, quantity = "sell", max_quantity_to_sell

        else:
            action, quantity = "hold", 0  # should do nothing

        #send_email(self.clients, action, quantity)
        return action, quantity