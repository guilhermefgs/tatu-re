from datetime import timedelta
from datetime import datetime
from talib import abstract
import pandas as pd

def calculate_indicators(df):
    """
    prediction_day: date in which the recomendation engine is used (datetime format)
    """
    # train_start = prediction_day - timedelta(days=120) #TODO define better this number
    # train_end = prediction_day
    # df = get_data(train_start, train_end)
    df = df.dropna()

    inputs = {
        'open': df["Open"],
        'high': df["High"],
        'low': df["Low"],
        'close': df["Close"],
        'volume': df["Volume"]
    }

    # Add all ta indicators    
    indicators = {

        # Trend indicators
        "SMA20": abstract.SMA(inputs, timeperiod=20), # Simple moving average over 20 days
        "SMA50": abstract.SMA(inputs, timeperiod=50), # Simple moving average over 50 days
        "SAR": abstract.SAR(inputs), # Parabolic stop and reverse

        # Volume indicators
        "OBV": abstract.OBV(inputs), # On balance volume
        "AD": abstract.AD(inputs), # Accumulation / Distribution indicator

        # Volatility indicators
        "ATR": abstract.ATR (inputs), # Average true range
        "NATR": abstract.NATR(inputs), # Normalized Average True Range
        "BBANDS ": abstract.BBANDS (inputs), # Bolinger bands
        
        # Momentum indicators
        "RSI": abstract.RSI (inputs), # Relative Strength Index
        "STOCHRSI": abstract.STOCHRSI(inputs), # Stochastic Relative Strength Index
        "MACD ": abstract.MACD(inputs), # Moving Average Convergence/Divergence
        "ULTOSC ": abstract.ULTOSC(inputs) # Ultimate Oscillator

        }

    pd.DataFrame.from_dict(indicators)
    
    return indicators

