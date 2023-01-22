
from datetime import datetime
from tatu_re.portfolio import Portfolio, Benchmark
from tatu_re.recommendation_engine import HiddenMarkovEngine
from tatu_re.utils import get_data

#------------- S&P Data - Simulation Date
start, end = datetime(2022,3,1), datetime(2022,3,28)
df = get_data(start, end)

#------------- Create Portfolio, Benchmark and Manager
benchmark = Benchmark(initial_capital=14000, start_date=start, timeseries=df["Open"])
portfolio = Portfolio(initial_capital=14000, start_date=start, benchmark=benchmark)
manager = HiddenMarkovEngine() # manager sends the email

#------------- Simulation

for index, row in df.iterrows():

    label, quantity = manager.recommendation(
        simulation_date=index, 
        price=row["Open"], 
        portfolio=portfolio,
        ticker="SPY"
    )

    portfolio.update(
        date=index,
        price=row["Open"],
        quantity=quantity,
        action=label
    )
predicted_ts = manager.model.save_predicted_timeseries()
#------------- Plot results
portfolio.plot(predicted_ts = predicted_ts)
