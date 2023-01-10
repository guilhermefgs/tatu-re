import pandas as pd
import numpy as np

def year_splitting(df):
    
    df['week_year'] = pd.DatetimeIndex(df.index).isocalendar().week
    unique_weeks = df['week_year'].unique()
    
    list_weeks = [df[df['week_year']==week] for week in unique_weeks]
    
    return list_weeks
