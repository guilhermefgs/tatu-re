import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from typing import List


class Portfolio:

    def __init__(self, initial_capital, start_date, benchmark) -> None:

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

        # benchmark
        self.benchmark = benchmark

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

    def plot(self) -> None:
        benchmark = self.benchmark.get_timeseries()
        total = np.add(self.in_cash_series, self.in_asset_series)
        self.plot_compare_benchmark(benchmark.index, total)
        self.plot_cash_vs_asset(benchmark.index)

    def plot_cash_vs_asset(self, timeindex) -> None:
        plt.figure(2, (16,8))
        plt.plot(timeindex, self.in_asset_series, "-b", label="In Asset")
        plt.plot(timeindex, self.in_cash_series, "-r", label="In Cash")
        plt.title("Cash flow of client point of view ($)", fontsize=20)
        plt.xlabel("Time (days)", fontsize=16)
        plt.ylim(0, 1500)
        plt.ylabel("Money ($)", fontsize=16)
        plt.legend(loc="lower left", fontsize=12)
        plt.grid()
        plt.show()
    
    def plot_compare_benchmark(self, timeindex, total):
        """Function that plots portfolio versus benchmark results in time
        """
        plt.figure(1, (16,8))
        plt.plot(timeindex, total, "-b", label="Your portfolio")
        plt.plot(timeindex, self.benchmark.get_timeseries(), "-r", label="S&P500 portfolio")
        plt.title("Portfolio Performance Comparison", fontsize=20)
        plt.xlabel("Time (days)", fontsize=16)
        plt.legend(loc="lower left", fontsize=12)
        plt.ylim(0, 1500)
        plt.ylabel("Money ($)", fontsize=16)
        plt.grid()
        plt.show()

class Benchmark:

    def __init__(self, initial_capital, start_date, timeseries) -> None:
        
        self.initial_capital: float = initial_capital
        self.start_date: datetime = start_date

        self.timeseries: pd.Series = timeseries

    def get_timeseries(self):
        price_first_day = self.timeseries[0]
        # initial capital needs to be higher than price
        max_n_stocks = self.initial_capital // price_first_day
        cash = self.initial_capital - (price_first_day * max_n_stocks)

        return (max_n_stocks * self.timeseries) + cash
