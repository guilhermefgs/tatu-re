from datetime import datetime, timedelta
import pandas as pd
from getFinancialData import getFinancialData
from run_model import decision
from Portfolio import Portfolio
import numpy as np


# TODO check numbers
def main():
    portfolio = Portfolio(1000, 0, 10)
    start = datetime(2020,3,1)
    end = datetime(2020,3,15)
    df = getFinancialData(start, end)


    delta = end - start # returns timedelta

    print("df.shape[0]: {}".format(df.shape[0]))
    for i in range(df.shape[0]):
        print("i: {}".format(i))
        day = start + timedelta(days=i)
        print(df["Close"].iloc[i])
        portfolio.update_price(df["Close"].iloc[i])
        [label, amount] = decision(df, None, 0, 1000)
        print("{} ${} in S&P".format(label, amount))
        n_units = amount // portfolio.unit_price
        if label == "buy":
            portfolio.buy(n_units)
        elif label == "sell":
            portfolio.sell(n_units)
        portfolio.append_day()
        print(portfolio.timeseries)
        print("mean {}".format(np.array(portfolio.timeseries).mean()))
        




if __name__ == "__main__":
    main()