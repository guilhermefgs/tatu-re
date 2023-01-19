from tatu_re.model.data_processing import calculate_target
from tatu_re.model.linear_regression import linear_regression_pipeline
from tatu_re.model.hmm import HMMStockPredictor
from tatu_re.model.utils import save_model
from tatu_re.utils import get_data

from datetime import datetime
import pathlib
import pickle

def train_data():
    begin = datetime(1980,3,1)
    end = datetime(2021,3,1)
    df = get_data(begin, end, "SPY")
    return df

def train_model(save=True):

    df = train_data()

    target = calculate_target(df["Close"])

    df = df.merge(target, how="right", left_index=True, right_index=True)

    y = df["target"]
    X = df.drop(["target"], axis=1)

    model = linear_regression_pipeline()

    model.fit(X, y)

    if save:
        save_model(filename="linear_regression_v1.sav", model=model)

    return model

def train_hidden_markov_model(save=True):
    
    # Initialise HMMStockPredictor object and fit the HMM
    model = HMMStockPredictor(train_data=train_data())
    model.fit()

    if save:
        save_model(filename="hmm_v1.sav", model=model)
