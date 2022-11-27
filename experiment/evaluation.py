from datetime import datetime, timedelta
import pandas as pd
from getFinancialData import getFinancialData
from run_model import decision
from Portfolio import Portfolio
import numpy as np
import matplotlib.pyplot as plt


# TODO check numbers
def main():

    start = datetime(2020,3,1)
    end = datetime(2020,3,30)
    df = getFinancialData(start, end)

    initial_money = 1000
    portfolio = Portfolio(initial_money, 0, 10)
    max_units = initial_money // df["Close"].iloc[0]
    SP500_portfolio = Portfolio(initial_money, 0, 10)

    print("df.shape[0]: {}".format(df.shape[0]))
    cash = []
    sandp = []
    for i in range(df.shape[0]):
        print("i: {}".format(i))
        day = start + timedelta(days=i)
        print(df["Close"].iloc[i])

        portfolio.update_price(df["Close"].iloc[i])
        [label, amount] = decision(df, None, portfolio.n_stocks*portfolio.unit_price, portfolio.total)
        print("{} ${} in S&P".format(label, amount))
        n_units = amount // portfolio.unit_price
        if label == "buy":
            portfolio.buy(n_units)
        elif label == "sell":
            portfolio.sell(n_units)
        cash.append(portfolio.in_cash)
        sandp.append(portfolio.n_stocks*portfolio.unit_price)
        portfolio.append_day()
        print("Your portfolio mean {}".format(np.array(portfolio.timeseries).mean()))
        print("{} of portfolio allocated in S&P".format(sandp[-1]))
        SP500_portfolio.update_price(df["Close"].iloc[i])
        if i == 1:
            SP500_portfolio.buy(max_units)
        SP500_portfolio.append_day()
        print("S&P500 portfolio mean {}".format(np.array(SP500_portfolio.timeseries).mean()))

    plt.figure(1, (16,8))
    plt.plot(portfolio.timeseries, "-b", label="Your portfolio")
    plt.plot(SP500_portfolio.timeseries, "-r", label="S&P500 portfolio")
    plt.title("Performance comparison")
    plt.xlabel("Time (days)")
    plt.legend(loc="lower left")
    plt.ylim(0, 1500)
    plt.ylabel("Money ($)")
    plt.grid()
    # plt.show()

    plt.figure(2, (16,8))
    plt.plot(cash, label="Cash")
    plt.plot(sandp, label="S&P")
    plt.legend()
    plt.grid()
    plt.show()
    

    


if __name__ == "__main__":
    main()