from datetime import datetime, timedelta
from utils import get_data, send_email
from experiment.portfolio import Portfolio
import numpy as np
from send_email import send_email


#-------------Get List of clients
clients = [
    {"Nome": "Christian", "Email": "christianleomil@gmail.com"},
    {"Nome": "Gui", "Email": "aateg.german@live.com"}
]

#-------------Read Financial Data
start = datetime(2020,3,1)
end = datetime(2020,3,30)
df = get_data(start, end)

initial_money = 1000
portfolio = Portfolio(initial_money, 0, 10)
max_units = initial_money // df["Close"].iloc[0]
SP500_portfolio = Portfolio(initial_money, 0, 10)

print("df.shape[0]: {}".format(df.shape[0]))
for i in range(df.shape[0]):
    print("i: {}".format(i))
    day = start + timedelta(days=i)
    print(df["Close"].iloc[i])

    portfolio.update_price(df["Close"].iloc[i])
    [label, amount] = decision(df, None, portfolio.n_stocks*portfolio.unit_price, portfolio.total)
    print("{} ${} in S&P".format(label, amount))
    if i == 0:
        send_email(clients, label, amount)
        
    n_units = amount // portfolio.unit_price
    if label == "buy":
        portfolio.buy(n_units)
    elif label == "sell":
        portfolio.sell(n_units)
    portfolio.append_day()
    print("Your portfolio mean {}".format(np.array(portfolio.timeseries).mean()))

    SP500_portfolio.update_price(df["Close"].iloc[i])
    if i == 1:
        SP500_portfolio.buy(max_units)
    SP500_portfolio.append_day()
    print("S&P500 portfolio mean {}".format(np.array(SP500_portfolio.timeseries).mean()))

#send_email(clients, label, amount)