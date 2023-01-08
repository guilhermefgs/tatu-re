import numpy as np
import pandas as pd
import statistics as st
import scipy.stats as sp

from tatu_re.utils import get_data
from tatu_re.model.data_processing import calculate_target

from datetime import timedelta, datetime

def evaluate_total():
    # get todays years with datetime
    today = datetime.today()
    year = today.year

    begin_year = year - timedelta(year=10)

    # generate list of years between begin_year and year
    years = [begin_year + timedelta(years=i) for i in range(year - begin_year + 1)]

    # evaluate each year
    pvalue_list = []
    conf_interval_list = []
    for year in years:
        pvalue, conf_interval = evaluate_one_year(year)
        pvalue_list.append(pvalue)
        conf_interval_list.append(conf_interval)

    return pvalue_list, conf_interval_list

def evaluate_one_year(model, year, ticker="DAX"):

    #-------Getting Data from S&P 500
    begin = datetime(year,1,1)
    end = datetime(year,12,31)
    df = get_data(begin, end, ticker)

    # -------Splitting timeseries into list of weeks
    df_splitted_in_weeks = year_splitting(df)

    #-------Simulate performance for selected period
    metric_model_list = []
    metric_benchmark_list = []
    n_days_list = np.array([])
    alfa = 0.05

    for df_week in df_splitted_in_weeks:

        y_predicted = model.predict(df_week)
        y_real = calculate_target(df)

        # calcula o AUC
        metric_model_list.append(metric(y_predicted))
        metric_benchmark_list.append(metric(y_real))
        n_days_list.append(len(df_week))

    
    metric_model_list_flat = [item for metric_model_list in l for item in metric_model_list]
    metric_benchmark_list_flat = [item for metric_benchmark_list in l for item in metric_benchmark_list]

    mean1 = st.fmean(metric_model_list_flat)
    mean2 = st.fmean(metric_benchmark_list_flat)

    n1=df.shape[0]
    n2=n1

    std1=st.stdev(metric_model_list_flat)
    std2=st.stdev(metric_benchmark_list_flat)

    SE=(((std1**2)/n1)+((std2**2)/n2))**0.5

    DF=(((std1**2)/n1 + (std2**2)/n2)**2) / ((1/(n1-1)*((std1**2)/n1)**2) + (1/(n2-1)*((std2**2)/n2)**2))

    TAlfaOver2=sp.t.ppf(1-alfa/2,DF)

    mean_upper=mean1-mean2+TAlfaOver2*SE
    mean_inferior=mean1-mean2-TAlfaOver2*SE

    tScore=(mean1-mean2)/SE
    pValue=2*(1 - sp.t.cdf(abs(tScore), DF))

    print('\n probability of occuring under H0 : '+'{:.2%}'.format(pValue))
    print('\n the mean range is : '+str(round(mean_inferior,2))+' to '+str(round(mean_upper,2))+'\n')

    conf_interval = (mean_inferior, mean_upper)
    return pValue, conf_interval

def year_splitting(df, year):
    
    df['week_year'] = pd.DatetimeIndex(df.index).isocalendar().week
    unique_weeks = df['week_year'].unique()
    
    list_weeks = [df[df['week_year']==week] for week in unique_weeks]
    
    return list_weeks

def metric(y):
    # compute cumulative returns from the y list
    cum_returns = np.cumprod(y + 1) - 1
    return cum_returns