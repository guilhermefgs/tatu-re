import numpy as np

def calculate_target(price, window=10, log=True):
    """Function that calculate target

    (price_ahead - price)/price

    price [window] days ahead minus price today

    :param price:
    :param log: return logaritmic difference
    """
    if log:
        return np.log(price / price.shift(-window))
    return (price - price.shift(-window)) / price