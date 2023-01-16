from tatu_re.model.data_processing import calculate_target
from tatu_re.model.gaussian_hmm import hmm_pipeline
from tatu_re.utils import get_data

from datetime import datetime
import pathlib
import pickle

def train_model(save=True):

    begin = datetime(2000,3,1)
    end = datetime(2021,3,1)
    df = get_data(begin, end)

    target = calculate_target(df["Close"])

    df = df.merge(target, how="right", left_index=True, right_index=True)

    y = df["target"]
    X = df.drop(["target"], axis=1)

    model = hmm_pipeline()

    model.fit(X)

    if save:
        filename = 'g_hmm_v2.sav'
        path = pathlib.Path(__file__).parent / "saved_models/"
        if not path.exists(): 
            path.mkdir()
        path_to_save = path / filename
        pickle.dump(model, open(path_to_save, 'wb'))

    return model
