import pandas as pd
import numpy as np
import statistics as st
import scipy.stats as sp
import pathlib

from tatu_re.utils import get_data
from tatu_re.evaluation.utils import year_splitting
from tatu_re.portfolio import Portfolio, Benchmark
from tatu_re.recommendation_engine import LinearRegressionEngine

from datetime import datetime

def evaluate_total():

    ticker="DAX.DE"

    # get todays years with datetime
    year = 2022
    years = np.arange(year, year + 1)

    # evaluate each year
    evaluation = []
    for year in years:
        pvalue, conf_interval = evaluate_one_year(year, ticker)
        evaluation.append(
            {
                "year": year,
                "ticker": ticker,
                "pValue": pvalue,
                "beginConfidenceInterval": conf_interval[0],
                "endConfidenceInterval": conf_interval[1],
            }
        )
        print(f"\n\nYear: {year} | p-value: {pvalue} | Confidence Interval: {conf_interval}")

    pd.DataFrame(evaluation).to_csv(pathlib.Path(__file__).parent / "results/evaluation_linear_regression_v1.csv", index=False)

def evaluate_one_year(year, ticker="DAX.DE"):

    #-------Getting Data from S&P 500
    begin = datetime(year,1,1)
    end = datetime(year,12,31)
    df = get_data(begin, end, ticker)

    # -------Splitting timeseries into list of weeks
    df_splitted_in_weeks = year_splitting(df)

    #-------Simulate performance for selected period
    model_results = []
    benchmark_results = []
    alfa = 0.05

    for i, df_week in enumerate(df_splitted_in_weeks):

        in_asset_series, in_cash_series, benchmark = simulate_portfolio(df_week, ticker)
        total = np.add(in_cash_series,in_asset_series)

        model_results.extend(total)
        benchmark_results.extend(benchmark)

    #-------Calculate metrics
    mean1 = st.fmean(model_results)
    mean2 = st.fmean(benchmark_results)

    n1=df.shape[0]
    n2=n1

    std1=st.stdev(model_results)
    std2=st.stdev(benchmark_results)

    SE=(((std1**2)/n1)+((std2**2)/n2))**0.5

    DF=(((std1**2)/n1 + (std2**2)/n2)**2) / ((1/(n1-1)*((std1**2)/n1)**2) + (1/(n2-1)*((std2**2)/n2)**2))

    TAlfaOver2=sp.t.ppf(1-alfa/2,DF)

    mean_upper=mean1-mean2+TAlfaOver2*SE
    mean_inferior=mean1-mean2-TAlfaOver2*SE

    tScore=(mean1-mean2)/SE
    pValue=2*(1 - sp.t.cdf(abs(tScore), DF))

    conf_interval = (mean_inferior, mean_upper)
    return pValue, conf_interval

def simulate_portfolio(df, ticker="DAX.DE"):

    begin_date = df.index[0]
    initial_capital = 10000

    benchmark = Benchmark(initial_capital=initial_capital, start_date=begin_date, timeseries=df['Close'])
    portfolio = Portfolio(initial_capital=initial_capital, start_date=begin_date, benchmark=benchmark)
    manager = LinearRegressionEngine()
    
    for index, row in df.iterrows():
    
        label, quantity = manager.recommendation(
            simulation_date = index, 
            price = row["Open"], 
            portfolio = portfolio, 
            ticker = ticker
        )
        
        portfolio.update(
            date=index,
            price=row["Open"],
            quantity=quantity,
            action=label
        )
    
    return portfolio.in_asset_series, portfolio.in_cash_series, portfolio.benchmark.get_timeseries()

if __name__ == "__main__":
    evaluate_total()
