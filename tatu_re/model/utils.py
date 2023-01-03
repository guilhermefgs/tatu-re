import pathlib
import pickle

def load_model(filename):
    """Load model from the disk

    :param filename: name of the file to be loaded, example: decision_tree_v1.sav
    :return: sklearn model object
    """
    if len(filename.split(".")) == 2:
        path = pathlib.Path(__file__).parent / f"saved_models/{filename}"
    elif len(filename.split(".")) == 1:
        path = pathlib.Path(__file__).parent / f"saved_models/{filename}.sav"
    else:
        raise NameError(f"Filename: {filename} is not correct.")
    if path.exists():
        return pickle.load(open(path, 'rb'))
    raise FileExistsError(f" File: {filename} doesn't exist in tatu_re/models")
