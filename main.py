
from datetime import datetime
from tatu_re.portfolio import Portfolio, Benchmark
from tatu_re.recommendation_engine import Monkey
from tatu_re.utils import get_data

#------------- S&P Data
start = datetime(2020,3,1)
end = datetime(2020,3,30)
df = get_data(start, end)

#------------- Create Portfolio, Benchmark and Manager
benchmark = Benchmark(initial_capital=1000, start_date=start, timeseries=df["Close"])
customer = Portfolio(initial_capital=1000, start_date=start, benchmark=benchmark)
manager = Monkey() # manager sends the email

#------------- Simulation

for index, row in df.iterrows():

    label, quantity = manager.recommendation(price=row["Close"], portfolio=customer)

    customer.update(
        date=index,
        price=row["Close"],
        quantity=quantity,
        action=label
    )

#------------- Plot results
customer.plot()
