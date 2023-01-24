import pandas as pd
import numpy as np
import statistics as st
import scipy.stats as sp
import pathlib
import matplotlib.pyplot as plt

from tatu_re.utils import get_data
from tatu_re.evaluation.utils import year_splitting
from tatu_re.portfolio import Portfolio, Benchmark
from tatu_re.recommendation_engine import LinearRegressionEngine
from tatu_re.recommendation_engine import HiddenMarkovEngine

from datetime import datetime

def evaluate_total():

    ticker="^N225"

    # get todays years with datetime
    year = 2013
    years = np.arange(year, year+10)

    # evaluate each year
    evaluation = []
    for year in years:
        pValue_Welch, conf_interval, means, variances, pValue_Levene, pValue_Wilcoxon = evaluate_one_year(year, ticker)
        evaluation.append(
            {
                "year": year,
                "ticker": ticker,
                "pValue Welch": pValue_Welch,
                "beginConfidenceInterval": conf_interval[0],
                "endConfidenceInterval": conf_interval[1],
                'mean model result': means[0],
                'mean benchamrk result':means[1],
                'variance model result': variances[0],
                'variance benchmark result': variances[1],
                'pValue Levene': pValue_Levene,
                'pValue Wilcoxon': pValue_Wilcoxon,
            }
        )
        print(f"\n\nYear: {year} | p-value Welch: {pValue_Welch} | Confidence Interval: {conf_interval}")
        print(f"\n\nYear: {year} | p-value Wilcoxon: {pValue_Wilcoxon} ")

    pd.DataFrame(evaluation).to_csv(pathlib.Path(__file__).parent / "results/evaluation_linear_regression_v1.csv", index=False)

def evaluate_one_year(year, ticker="^N225"):

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

    #-------General Data
    means=[np.mean(model_results),np.mean(benchmark_results)]
    standard_dev=[np.std(model_results),np.std(benchmark_results)]
    print(standard_dev)
    variances=[x**2 for x in standard_dev]

    #-------Welch unpooled test
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
    pValue_Welch=2*(1 - sp.t.cdf(abs(tScore), DF))

    conf_interval = (mean_inferior, mean_upper)
    #-------Levene test

    stats_Levene,pValue_Levene=sp.levene(model_results,benchmark_results,center='median')

    #-------Wilcoxon test
    stats_Wilcoxon,pValue_Wilcoxon=sp.wilcoxon(model_results,benchmark_results)

    #-------Box plot
    fig, ax = plt.subplots()
    ax.boxplot([model_results, benchmark_results], labels=['Model Results', 'Benchmark Results'])
    plt.title('Box Plots of Two Distributions')
    plt.savefig('C:/Users/chris/OneDrive/Documentos/GitHub/tatu-re/tatu_re/evaluation/results/box plot-'+str(year))
    plt.close()

    #-------Quantile Quantile Plots 
    plt.figure()
    sp.probplot(model_results, dist="norm", plot=plt)
    plt.title("Q-Q Model Results")
    plt.savefig('C:/Users/chris/OneDrive/Documentos/GitHub/tatu-re/tatu_re/evaluation/results/QQ Model-'+str(year))
    plt.close()

    plt.figure()
    sp.probplot(benchmark_results, dist="norm", plot=plt)
    plt.title("Q-Q Benchmark")
    plt.savefig('C:/Users/chris/OneDrive/Documentos/GitHub/tatu-re/tatu_re/evaluation/results/QQ Benchmark-'+str(year))
    plt.close()

    return pValue_Welch, conf_interval, means, variances, pValue_Levene, pValue_Wilcoxon

def simulate_portfolio(df, ticker="^N225"):

    begin_date = df.index[0]
    initial_capital = 100000

    benchmark = Benchmark(initial_capital=initial_capital, start_date=begin_date, timeseries=df['Close'])
    portfolio = Portfolio(initial_capital=initial_capital, start_date=begin_date, benchmark=benchmark)
    manager = HiddenMarkovEngine()
    # manager = LinearRegressionEngine()
    
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
