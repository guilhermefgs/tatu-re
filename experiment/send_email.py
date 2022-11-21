# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 17:12:52 2022

@author: chris
"""

import yfinance as yf

data = yf.download(tickers='SPY', period='5y',interval='1d')