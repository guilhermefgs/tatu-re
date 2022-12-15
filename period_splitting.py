# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 08:54:41 2022

@author: chris
"""

import numpy as np
import pandas as pd

def year_splitting(df,year):
    
    df.index = df.index.tz_localize(None)
    df['row number']=np.arange(df.shape[0])
    df['year']=pd.DatetimeIndex(df.index).year
    df['week of year']=pd.DatetimeIndex(df.index).isocalendar().week
    df=df[df['year']==year]
    
    unique=df['week of year'].unique()
    
    list_of_periods=[]
    for i in unique:
        list_of_periods.append(df[df['week of year']==i])
    
    return list_of_periods

def date_selection(df,start,end,list_of_days,number_of_days):
    
    df.index = df.index.tz_localize(None) # removes timezone from index that contains date and time
    df['row number']=np.arange(df.shape[0])
    
    list_of_days=df[df.index.isin(list_of_days)]['row number'].tolist()
    
    list_of_periods=[]
    
    for i,x in enumerate(list_of_days): 
        list_of_days[i]=list(range(x,x+number_of_days))
        list_of_periods.append(df[df['row number'].isin(list_of_days[i])])
    
    return list_of_periods