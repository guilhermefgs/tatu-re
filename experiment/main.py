
from datetime import datetime
from portfolio import Portfolio
from recommendation_engine import Monkey
from utils import get_data

#------------- S&P Data
start = datetime(2020,3,1)
end = datetime(2020,3,30)
df = get_data(start, end)

#------------- Create Portfolio and Manager
customer = Portfolio(initial_capital=1000, start_date=start)
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
#print(customer.operations)
customer.plot()
