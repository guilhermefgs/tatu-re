import numpy as np
import pandas as pd

def calculate_target(price, window=10, log=True):
    """Function that calculate target

    (price_ahead - price)/price

    price [window] days ahead minus price today

    :param price:
    :param log: return logaritmic difference
    """
    if log:
        s = np.log(price.shift(-window)/price)
    else:
        s = (price.shift(-window) - price) / price
    return pd.Series(s, name="target")