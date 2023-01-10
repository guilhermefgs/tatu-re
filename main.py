
from datetime import datetime
from tatu_re.portfolio import Portfolio, Benchmark
from tatu_re.recommendation_engine import LinearRegressionEngine, HMMEngine
from tatu_re.utils import get_data

#------------- S&P Data - Simulation Date
start = datetime(2021,4,11)
end = datetime(2021,6,15)
df = get_data(start, end)

#------------- Create Portfolio, Benchmark and Manager
benchmark = Benchmark(initial_capital=1400, start_date=start, timeseries=df["Close"])
portfolio = Portfolio(initial_capital=1400, start_date=start, benchmark=benchmark)
manager = HMMEngine() # manager sends the email

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
portfolio.plot()
