import numpy as np
import pandas as pd
from datetime import datetime
from tatu_re.portfolio import Portfolio, Benchmark
from tatu_re.recommendation_engine import LinearRegressionEngine
from tatu_re.utils import get_data

#------------- S&P Data - Simulation Date
start = datetime(2023,1,1)
end = datetime(2023,2,1)
df = get_data(start, end)

#------------- Create Portfolio, Benchmark and Manager
benchmark = Benchmark(initial_capital=1400, start_date=start, timeseries=df["Close"])
portfolio = Portfolio(initial_capital=1400, start_date=start, benchmark=benchmark)
manager = LinearRegressionEngine() # manager sends the email

#------------- Simulation

for index, row in df.iterrows():

    label, quantity = manager.recommendation(
        simulation_date=index, 
        price=row["Open"], 
        portfolio=portfolio
    )

    print(f"Decision={label} | quantity={quantity}\n\n")

    portfolio.update(
        date=index,
        price=row["Open"],
        quantity=quantity,
        action=label
    )

#------------- Plot results
portfolio.save_cash_vs_asset()
portfolio.plot()
# portfolio.benchmark.get_timeseries().to_csv("timeseries.csv")

total = np.add(portfolio.in_cash_series, portfolio.in_asset_series)

total_df = pd.DataFrame()
total_df["Date"] = portfolio.benchmark.get_timeseries().index
total_df["Close"] = total
total_df.to_csv("timeseries.csv")