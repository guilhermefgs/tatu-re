import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
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
            self.in_asset += amount
            self.n_stocks += quantity
        elif action == "sell":
            self.in_cash += amount
            self.in_asset -= amount
            self.n_stocks -= quantity
        self.in_cash_series.append(self.in_cash)
        self.in_asset_series.append(self.in_asset)

    def plot(self) -> None:
        
        total = np.add(self.in_cash_series, self.in_asset_series)
        print(total)
        #benchmark = How to simulate
        timeindex = [self.start_date - timedelta(days=x) for x in range(len(total))]

        self.plot_in_cash_vs_asset(timeindex)

    def plot_in_cash_vs_asset(self, timeindex) -> None:
        plt.figure(1, (16,8))
        plt.plot(timeindex, self.in_asset_series, "-b", label="In Asset")
        plt.plot(timeindex, self.in_cash_series, "-r", label="In Cash")
        plt.title("Cash flow of client point of view ($)", fontsize=20)
        plt.xlabel("Time (days)", fontsize=16)
        plt.ylim(0, 1500)
        plt.ylabel("Money ($)", fontsize=16)
        plt.legend(loc="lower left", fontsize=12)
        plt.grid()
        plt.show()


    def compare_benchmark(self):
        pass


def plot_benchmark_comparison(portfolio, benchmark, time_index) -> None:
    """Function that plots portfolio versus benchmark results in time
    :param portfolio: customer portfolio series
    :param benchmark: benchmark series
    """
    plt.figure(1, (16,8))
    plt.plot(time_index, portfolio, "-b", label="Your portfolio")
    plt.plot(time_index, benchmark, "-r", label="S&P500 portfolio")
    plt.title("Performance Comparison", fontsize=20)
    plt.xlabel("Time (days)", fontsize=16)
    plt.legend(loc="lower left", fontsize=12)
    plt.ylim(0, 1500)
    plt.ylabel("Money ($)", fontsize=16)
    plt.grid()
    plt.show()

def plot_cash(cash, sandp, time_index):

    plt.figure(2, (16,8))
    plt.plot(time_index, cash, label="Cash")
    plt.plot(time_index, sandp, label="S&P")
    plt.title("Cash flow from client point of view ($)", fontsize=20)
    plt.xlabel("Time (days)", fontsize=16)
    plt.ylabel("Money ($)", fontsize=16)
    plt.legend(fontsize=12)
    plt.grid()
    plt.show()
