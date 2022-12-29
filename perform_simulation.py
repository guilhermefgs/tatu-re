# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 09:07:25 2022

@author: chris
"""

import numpy as np
from tatu_re.portfolio import Portfolio,Benchmark
from tatu_re.recommendation_engine import MonkeyEvolution
from tatu_re.recommendation_engine import Monkey

def simulates_portfolio_once(chosen_date,df):
    
    benchmark = Benchmark(initial_capital=1000,start_date=chosen_date,timeseries=df['Close'])
    portfolio = Portfolio(initial_capital=1000,start_date=chosen_date,benchmark=benchmark)
    manager = MonkeyEvolution()
    # manager = Monkey()
    
    for index, row in df.iterrows():
    
        label, quantity = manager.recommendation(price=row["Close"], portfolio=portfolio)
        
        portfolio.update(
            date=index,
            price=row["Close"],
            quantity=quantity,
            action=label
        )
    
    # ------------- Plot results
    # portfolio.plot()
    
    [in_asset_series,in_cash_series,benchmark]=portfolio.return_variables()
    
    return in_asset_series,in_cash_series,benchmark

def simulation_loop(list_of_periods,number_of_experiments):
    
    list_diff_AUC=[]
    list_check_in_asset=[]
    list_check_in_cash=[]
    list_check_benchmark=[]
    list_check_total=[]
    for i in list(range(0,number_of_experiments)):
        list_partial=[]
        
        list_parcial_check_in_asset=[]
        list_parcial_check_in_cash=[]
        list_parcial_check_benchmark=[]
        list_parcial_total=[]
        
        for j in list_of_periods:        
            [in_asset_series,in_cash_series,benchmark]=simulates_portfolio_once(j.index[0],j)
            
            total=np.add(in_cash_series,in_asset_series)
            list_parcial_total.append(total)
            list_partial.append((total.sum()-benchmark.sum())/(len(total)))
            
            list_parcial_check_in_asset.append(in_asset_series)
            list_parcial_check_in_cash.append(in_cash_series)
            list_parcial_check_benchmark.append(benchmark)
            
        list_diff_AUC.append(list_partial)
        
        list_check_in_asset.append(list_parcial_check_in_asset)
        list_check_in_cash.append(list_parcial_check_in_cash)
        list_check_benchmark.append(list_parcial_check_benchmark)
        list_check_total.append(list_parcial_total)
        
    
    return list_diff_AUC,list_check_in_asset,list_check_in_cash,list_check_benchmark,list_check_total