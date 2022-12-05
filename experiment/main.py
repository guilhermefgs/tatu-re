# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 09:13:46 2022

@author: chris
"""

import pandas as pd
import send_email
import getFinancialData
import machineLearning


#-------------Get List of clients
dfClients=pd.read_excel('listOfClients.xlsx')


#-------------Read Financial Data
dateStart="1998-12-01"
dateStop="2022-01-01"

dfFinancial=getFinancialData.getFinancialData(dateStart,dateStop)

#-------------Analyse Historical Data
[action,dfAmount]=machineLearning.machineLearning(dfFinancial,dfClients)

#-------------Send Email with action
amount='1000'

send_email.send_email(dfClients,action,amount)