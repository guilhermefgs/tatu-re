import pathlib
import pickle
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error

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

def calc_mse(input_df):
    """
    Calculates the Mean Squared Error between real and predicted close prices
    :param input_df: Pandas Dataframe containing the data, actual close prices, and predicted close prices
    :return: Mean Squared Error
    """
    actual_arr = (input_df.loc[:, "Actual_Close"]).values
    pred_arr = (input_df.loc[:, "Predicted_Close"]).values
    mse = mean_squared_error(actual_arr, pred_arr)
    return mse


def plot_results(in_df, out_dir, stock_name):
    """
    Plots the results for historical predictions
    :param in_df: Pandas Dataframe containing the data, actual close prices, and predicted close prices
    :param out_dir: Output directory
    :param stock_name: Stock name found in original input
    :return: Plot comparing the two sets of data is shown and saved.
    """
    in_df = in_df.reset_index()  # Required for plotting
    ax = plt.gca()
    in_df.plot(kind="line", x="Date", y="Actual_Close", ax=ax)
    in_df.plot(kind="line", x="Date", y="Predicted_Close", color="red", ax=ax)
    plt.ylabel("Daily Close Price (in USD)")
    plt.title(str(stock_name) + " daily closing stock prices")
    save_dir = f"{out_dir}/{stock_name}_results_plot.png"
    plt.savefig(save_dir)
    plt.show()
    plt.close("all")
