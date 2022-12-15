from ta.trend import sma_indicator, psar_up, psar_down
from ta.volume import on_balance_volume, acc_dist_index
from ta.volatility import average_true_range, bollinger_mavg
from ta.momentum import rsi, stoch, ultimate_oscillator
from tatu_re.utils import get_data
from datetime import timedelta, datetime

import pandas as pd

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Function to calculate indicators

    Trend Indicators
    - SMA20: Simple moving average with 20 days window
    - SMA50: Simple moving average with 50 days window
    - PSAR_UP: Parabolic stop and reverse for upward trends
    - PSAR_DOWN: Parabolic stop and reverse for downward trends

    Volume Indicators
    - OBV: On balance volume
    - AD: Accumulation / Distribution indicator

    Volatility Indicators
    - ATR: Average true range
    - BBANDS: Bollinger Bands with 20 days simple moving average (MA).

    Momentum Indicators
    - RSI: Relative Strength Index
    - STOCHRSI: Stochastic Relative Strength Index
    - ULTOSC: Ultimate Oscillator

    :param df: DataFrame of the security, given by Yfinance
    :return: DataFrame with all new series of indicators

    """

    df = df.dropna()
    high = df["High"]
    low = df["Low"]
    close = df["Close"]
    volume=df["Volume"]

    # Add all ta indicators    
    indicators = {

        # Trend indicators
        "SMA20": sma_indicator(close, window=20),
        "SMA50": sma_indicator(close, window=20),
        "PSAR_UP": psar_up(high, low, close),
        #"PSAR_DOWN": psar_down(high, low, close),
        
        # Volume indicators
        "OBV": on_balance_volume(close, volume),
        "AD": acc_dist_index(high, low, close, volume),

        # Volatility indicators
        "ATR": average_true_range(high, low, close),
        "BBANDS ": bollinger_mavg(close),
        
        # Momentum indicators
        "RSI": rsi(close),
        "STOCHRSI": stoch(high, low, close),
        "ULTOSC ": ultimate_oscillator(high, low, close) 

    }
    
    return pd.DataFrame.from_dict(indicators)

def calculate_features(date: datetime) -> pd.DataFrame:

    df = get_data(start=(date-timedelta(days=100)), end=date)
    return calculate_indicators(df.iloc[:-1]).fillna(0)
