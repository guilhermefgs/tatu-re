class Portfolio:
    
    def __init__(self, total=0, n_stocks=0, unit_price=0):
        """
        total: Total in cash + stock value
        n_stocks: number of stocks in portfolio
        in_cash: cash in portfolio
        unit_price: (current) price of stock unit
        timeseries: timeseries of portfolio performance over days
        """

        # TODO buy units
        self.total = total
        self.n_stocks = n_stocks
        self.unit_price = unit_price
        self.in_cash = self.total - self.n_stocks*self.unit_price
        self.timeseries = [] # TODO make this an actual timeseries

    def buy(self, n_units):
        self.in_cash -= n_units*self.unit_price
        self.n_stocks += n_units

    def sell(self, n_units):
        self.in_cash += n_units*self.unit_price
        self.n_stocks -= n_units

    def update_price(self, new_price):
        self.unit_price = new_price
        self.total = self.in_cash + self.n_stocks*self.unit_price

    def append_day(self):
        self.timeseries.append(self.total)
