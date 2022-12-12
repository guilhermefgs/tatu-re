from indicators import calculate_indicators
from target import calculate_target
from utils import get_data

from sklearn.tree import DecisionTreeRegressor

from datetime import datetime
import pathlib
import pickle

def train_set():
    begin = datetime(2015,3,1)
    end = datetime(2020,3,1)
    df = get_data(begin, end)

    indicators = calculate_indicators(df)
    target = calculate_target(df["Open"])

    merged_df = indicators.merge(target, how="inner", left_index=True, right_index=True)
    merged_df_droped_na = merged_df.dropna()

    y = merged_df_droped_na["target"]
    X = merged_df_droped_na.drop("target", axis=1)
    return X, y

def train_model(X_train, y_train, save=False):

    model = DecisionTreeRegressor()

    model.fit(X_train, y_train)

    if save:
        filename = 'decision_tree_v1.sav'
        path = pathlib.Path(__file__).parent / "models/"
        if not path.exists(): 
            path.mkdir()
        path_to_save = path / filename
        pickle.dump(model, open(path_to_save, 'wb'))

    return model

def load_model(filename):
    """Load model from the disk

    :param filename: name of the file to be loaded, example: decision_tree_v1.sav
    :return: sklearn model object
    """
    path = pathlib.Path(__file__).parent / f"models/{filename}"
    if path.exists():
        return pickle.load(open(path, 'rb'))
    raise FileExistsError(f" File: {filename} doesn't exist in tatu_re/models")

if __name__ == "__main__":
    X, y = train_set()
    model = train_model(X, y, save=True)