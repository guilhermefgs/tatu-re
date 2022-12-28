import pandas as pd

from datetime import datetime
from tatu_re.utils import get_data

class Benchmark:

    def __init__(self, timeseries) -> None:
        self.timeseries: pd.Series = timeseries

    @classmethod
    def from_dates(cls, start: datetime, end: datetime):
        return cls(get_data(start, end))

    def cumprod_returns(self):
        return (1 + self.timeseries.pct_change()).cumprod()
