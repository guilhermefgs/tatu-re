import numpy as np
import matplotlib.pyplot as plt

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
    plt.ylim(800, 2000)
    plt.ylabel("Money ($)", fontsize=16)
    plt.grid()
    plt.show()