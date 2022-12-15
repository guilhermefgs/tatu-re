# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 22:40:54 2022

@author: chris
"""

from datetime import datetime
from tatu_re.utils import get_data
import period_splitting
import perform_simulation
import analyse_data

#-----------S&P DAta
ticker="DAX.DE" #SPY for S&P 500, DAX.DE for DAX
start = datetime(1994,3,1)
end=datetime.today()
number_of_days=100
number_of_experiments=100
year=2020

# list_of_days=['2020-01-10','1998-10-02','2002-08-01','1995-05-01','2021-04-05','2022-06-01','1997-05-01'] #SnP
# list_of_days=['2008-01-17','2012-09-24','2015-09-10','2017-03-20','2018-10-31','2008-01-22','2021-09-07'] #DAX.DE
# list_of_days=['2020-01-10','1998-10-02','2002-08-01']
# list_of_days=['2020-01-10','1998-10-02','2002-08-01']
list_of_days=['2015-03-16','2020-01-22','2008-01-09','2011-04-05'] # low levels for DAX



#-------Getting Data from S&P 500
df = get_data(start,end,ticker)
df.index = df.index.tz_localize(None)
df.to_excel('C:/Users/chris/OneDrive/Documentos/GitHub/tatu-re/'+'df.xlsx')



#-------Splitting timeseries into periods for comparison of performance
list_of_periods=period_splitting.date_selection(df, start, end, list_of_days, number_of_days)
# list_of_periods=period_splitting.year_splitting(df,year)



#-------Simulate performance for selected period
[list_diff_AUC,list_check_in_asset,
 list_check_in_cash,list_check_benchmark]=perform_simulation.simulation_loop(list_of_periods,number_of_experiments)



#-------analysing output data, plotting charts and testing type 1 and type 2 error
[list_mean,list_std_dev,list_z_type1,list_diff_AUC2]=analyse_data.error_type1_testing(list_diff_AUC)


print(sum(i>2.33 for i in list_z_type1)/len(list_z_type1))
print(sum(i<-2.33 for i in list_z_type1)/len(list_z_type1))
print((sum(i>2.33 for i in list_z_type1)+sum(i<-2.33 for i in list_z_type1))/len(list_z_type1))

