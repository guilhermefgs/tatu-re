
import numpy as np
import pandas as pd
from datetime import datetime

import streamlit as st

from tatu_re.utils import get_data

# st.title("My Portfolio")
st.set_page_config(
    page_title="Tatu RE",
    page_icon=":octopus:"
)

st.markdown("# Tatu RE - Portfolio")

col1, col2 = st.columns(2)

col1.markdown("""

## Indicators

""")

col2.selectbox("Time Range", ["Weekly", "2 Weeks", "Monthly", "Yearly"]) # TODO implement different time ranges

p_value, return_metric, return_sp = st.columns(3)

st.markdown("""

## Performance Over Time

""")

## Load Data 
start = datetime(2022,10,11)
end = datetime(2022,12,15) # TODO make sure to query the same interval of S&P as the data in the csv file
benchmark = get_data(start, end)["Close"].rename("S&P")

performance = pd.read_csv("timeseries.csv", index_col="Date")["Close"]
performance = performance.rename("Portfolio")
performance.index = pd.to_datetime(performance.index)


# Update absolute metrics value
p_value.metric("Portfolio Value", "$ {:.2f} ".format(performance.iloc[-1]), delta="$ {:.2f} ".format(performance.iloc[-1] - performance.iloc[0]))

# Normalize
benchmark = (benchmark/benchmark.iloc[0] - 1)*100
performance = (performance/performance.iloc[0] - 1)*100

# Update percentual metrics
return_metric.metric("Return", "{:.2f} %".format(performance[-1]))
return_sp.metric("S&P Return", "{:.2f} %".format(benchmark[-1]))

df = pd.concat([benchmark, performance], axis=1, sort=True)

fig = st.line_chart(df)

# TODO add portfolio composition chart