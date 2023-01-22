import warnings
import logging
import itertools
import numpy as np

from hmmlearn.hmm import GaussianHMM
from datetime import timedelta

from tatu_re.utils import get_data

# Suppress warning in hmmlearn
warnings.filterwarnings("ignore")

class HMMStockPredictor:
    def __init__(
        self,
        train_data,
        n_hidden_states=10,
        n_latency_days=10,
    ):
        self._init_logger()
        self.n_latency_days = n_latency_days
        self.hmm = GaussianHMM(n_components=n_hidden_states)
        self.train_data = train_data
        self.timeseries = []


    def save_predicted_timeseries(self):
        # self.timeseries.to_csv("predicted_timeseries.csv")
        return self.timeseries

    def _init_logger(self):
        self._logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)


    def fit(self):
        """Fit the continuous emission Gaussian HMM."""
        self._logger.info(">>> Extracting Features")
        observations = HMMStockPredictor._extract_features(self.train_data)
        self._logger.info("Features extraction Completed <<<")
        # Fit the HMM using the fit feature of hmmlearn
        self.hmm.fit(observations)


    @staticmethod
    def _extract_features(data):
        """Extract the features - open, close, high, low price - from the Yahooo finance generated dataframe."""
        open_price = np.array(data["Open"])
        close_price = np.array(data["Close"])
        high_price = np.array(data["High"])
        low_price = np.array(data["Low"])

        # We compute the fractional change in high,low and close prices to use as our set of observations
        frac_change = (close_price - open_price) / open_price
        frac_high = (high_price - open_price) / open_price
        frac_low = (open_price - low_price) / open_price

        # Put the observations into one array
        return np.column_stack((frac_change, frac_high, frac_low))


    def predict(self, prediction_day, ticker="SPY"):
        # Use the previous n_latency_days worth of data for predictions
        start, end = prediction_day - timedelta(days=self.n_latency_days), prediction_day

        predict_data = get_data(start, end, ticker)

        # avoiding problem with simulation
        if prediction_day in predict_data.index:
            predict_data = predict_data.iloc[:-1]
        predicted_frac_change, score = self._get_most_probable_outcome(predict_data)

        self.timeseries.append(predict_data.iloc[-1]["Open"]*(1+predicted_frac_change))

        return predicted_frac_change, score


    def _get_most_probable_outcome(self, predict_data):
        """
        Using the fitted HMM, calculate the most probable outcome for a given day (e.g. prices will rise by 0.01).
        :param predict_data: DataFrame for prediction last day - latency days
        :return: The HMM's predicted movements in frac_change, frac_high, frac_low
        """
        features = HMMStockPredictor._extract_features(predict_data)

        outcome_score = []

        # Score all possible outcomes and select the most probable one to use for prediction
        possible_outcomes = self._compute_all_possible_outcomes()
        
        for possible_outcome in possible_outcomes:
            total_data = np.row_stack((features, possible_outcome))
            outcome_score.append(self.hmm.score(total_data))

        print(np.max(outcome_score))
        # Get the index of the most probable outcome and return it
        most_probable_outcome = possible_outcomes[np.argmax(outcome_score)]

        return most_probable_outcome[0], np.max(outcome_score)


    def _compute_all_possible_outcomes(
        self, n_intervals_frac_change=50, n_intervals_frac_high=10, n_intervals_frac_low=10
    ):
        """Creates np arrays with evenly  spaced numbers for each range."""
        frac_change_range = np.linspace(-0.1, 0.1, n_intervals_frac_change)
        frac_high_range = np.linspace(0, 0.1, n_intervals_frac_high)
        frac_low_range = np.linspace(0, 0.1, n_intervals_frac_low)

        return np.array(
            list(itertools.product(frac_change_range, frac_high_range, frac_low_range))
        )