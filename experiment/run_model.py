import pandas as pd
import numpy as np

def main():
    df = pd.DataFrame()
    model = None
    action = decision(df, None, in_asset = 100, total=1000)


def decision(x, model, in_asset, total):
    '''
    Function that returns the recommended action (buy/sell/hold, amount) given the model inputs and the model itself
    x: inputs from the model - a priori time series data
    model: model object
    amount: amount of unit stocks in the portfolio; limits how much is possible to sell
    '''
    # TODO read model and do prediction = model.predict(x)
    
    prediction = np.random.uniform(-1, 1)

    label = "buy" if prediction > 0.3 else ("sell" if prediction < -0.3 else "hold")

    if label == "sell":
        return label, min(abs(prediction)*total, in_asset)
    elif label == "buy":
        return  label, min(abs(prediction)*total, total-in_asset) 
    
    return label, 0

if __name__ == "__main__":
    main()