# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 09:19:51 2022

@author: chris
"""

import yfinance as yf

def getFinancialData(dateStart,dateStop):
    """
    dateStart, dateStop: date start and end in string YYYY-MM-DD or datetime format
    """
    spyticker = yf.Ticker("SPY")
    dfFinancial= spyticker.history(period="max", interval="1d", 
                                   start=dateStart, end=dateStop, 
                                   auto_adjust=True, rounding=True)
    return dfFinancial