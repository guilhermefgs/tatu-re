import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from tatu_re.utils import send_email, get_data
from tatu_re.portfolio import Portfolio
from tatu_re.model import load_model
from typing import Tuple
from datetime import timedelta

class RecommendationEngine(ABC):

    def __init__(self):
        self.clients = pd.DataFrame([
            {"Nome": "Christian", "Email": "christianleomil@gmail.com"},
            {"Nome": "Gui", "Email": "aateg.german@gmail.com"}
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
        
class LinearRegressionEngine(RecommendationEngine):
    """Recommendation Engine based on Linear Regression model
    """
    model = load_model("linear_regression_v1.sav")

    def recommendation(self, simulation_date, price, portfolio, ticker):

        df = get_data(
            start = simulation_date - timedelta(days=100),
            end =  simulation_date,
            ticker = ticker
        )
        
        u = self.model.predict(df)[-1]

        action = "buy" if u > 0.01 else ("sell" if u < -0.01 else "hold")

        action, quantity = self.criteria_for_quantity_of_investment(action, price, portfolio)

        self.send_email(action, quantity)

        return action, quantity


class HiddenMarkovEngine(RecommendationEngine):
    """Recommendation Engine based on Hidden Markov Model
    """
    model = load_model("hmm_v2_10_hidden_31635_963689263845_score.sav")

    def recommendation(self, simulation_date, price, portfolio, ticker):
        u, high, low, score = self.model.predict(simulation_date, ticker)
        print(f"u: {u}; score: {score}")
        rec_thresh = 0.005
        
        if high > low :
            if u > rec_thresh:
                action = "buy"
            elif u < rec_thresh:
                action = "sell"
            else:
                action = "hold"
        else:
            action = "sell"

        # action = "buy" if u > rec_thresh else "sell" if u < -rec_thresh else "hold"
        
        _action, quantity = self.criteria_for_quantity_of_investment(action, price, portfolio, score)

        self.send_email(action, quantity)

        print(f"Action={action}, Decision={_action} | quantity={quantity}\n\n")

        return _action, quantity

    def criteria_for_quantity_of_investment(self, action: str, price: float, portfolio: Portfolio, score: float):
        # assert score > 0

        if score > -20:
            
            certainty = max(min(score/50, 1), 0.2)
            print(certainty)
            if action == "buy":
                max_quantity_to_buy = portfolio.in_cash*certainty // price
                if max_quantity_to_buy == 0:
                    action, quantity = "hold", 0 # don't have enough money to execute order
                else:
                    action, quantity = "buy", max_quantity_to_buy

            elif action == "sell":
                max_quantity_to_sell = portfolio.n_stocks // (1/certainty)
                if max_quantity_to_sell == 0:
                    action, quantity = "hold", 0  # don't have any stock to share
                else:
                    action, quantity = "sell", max_quantity_to_sell

            else:
                action, quantity = "hold", 0  # should do nothing
        else:
            action, quantity = "hold", 0  # should do nothing
        
        return action, quantity