
from datetime import datetime
from tatu_re.portfolio import Portfolio, Benchmark
from tatu_re.recommendation_engine import HiddenMarkovEngine
from tatu_re.utils import get_data

#------------- S&P Data - Simulation Date
start, end = datetime(2022,11,1), datetime(2022,12,31)
df = get_data(start, end)

#------------- Create Portfolio, Benchmark and Manager
benchmark = Benchmark(initial_capital=1400, start_date=start, timeseries=df["Close"])
portfolio = Portfolio(initial_capital=1400, start_date=start, benchmark=benchmark)
manager = HiddenMarkovEngine() # manager sends the email

#------------- Simulation

for index, row in df.iterrows():

    label, quantity = manager.recommendation(
        simulation_date=index, 
        price=row["Close"], 
        portfolio=portfolio,
        ticker="SPY"
    )

    portfolio.update(
        date=index,
        price=row["Close"],
        quantity=quantity,
        action=label
    )

#------------- Plot results
portfolio.plot()
