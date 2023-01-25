import pandas as pd
import numpy as np

def year_splitting(df):
    
    df['week_year'] = pd.DatetimeIndex(df.index).isocalendar().week
    unique_weeks = df['week_year'].unique()
    
    # Create range of two-week intervals
    two_week_intervals = pd.date_range(df.index[0], df.index[-1], freq='2W')

    # Find indices of original DataFrame that correspond to start of each interval
    indices = pd.DatetimeIndex(df.index).searchsorted(two_week_intervals)

    # Create list of DataFrame slices for each interval
    list_weeks = [df.iloc[indices[i]:indices[i+1]] for i in range(len(indices)-1)]

    # list_weeks = [df[df['week_year']==week] for week in unique_weeks]
    
    return list_weeks
