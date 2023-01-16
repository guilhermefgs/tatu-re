"""
Usage:
stock_analysis.py --n=<stock_name> --s<start_date> --e<end_date> --o<out_directory> --p<plot> --f<future> --m<metric>
"""
import warnings
import logging
import itertools
import pandas as pd
import numpy as np
from tatu_re.utils import get_data

from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import train_test_split

from tqdm import tqdm

import sys

from datetime import timedelta

# Suppress warning in hmmlearn
warnings.filterwarnings("ignore")


class HMMStockPredictor:
    def __init__(
        self,
        start_date,
        end_date,
        future_days,
        test_size=0.33,
        n_hidden_states=4,
        n_latency_days=10,
        n_intervals_frac_change=50,
        n_intervals_frac_high=10,
        n_intervals_frac_low=10,
    ):
        self._init_logger()
        self.company = "SPY"
        self.start_date = start_date
        self.end_date = end_date
        self.n_latency_days = n_latency_days
        self.hmm = GaussianHMM(n_components=n_hidden_states)
        self._split_train_test_data(test_size)
        self._compute_all_possible_outcomes(
            n_intervals_frac_change, n_intervals_frac_high, n_intervals_frac_low
        )
        self.predicted_close = None
        self.days_in_future = future_days

    def _init_logger(self):
        self._logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)

    def _split_train_test_data(self, test_size):
        """Downloads data and splits it into training and testing datasets."""
        # Download data
        used_data = get_data(self.start_date, self.end_date, self.company)

        # Do not shuffle the data as it is a time series
        _train_data, test_data = train_test_split(
            used_data, test_size=test_size, shuffle=False
        )
        self.train_data = _train_data
        self.test_data = test_data

        # Drop the columns that aren't used
        self.train_data = self.train_data.drop(["Volume", "Adj Close"], axis=1)
        self.test_data = self.test_data.drop(["Volume", "Adj Close"], axis=1)

        # Set days attribute
        self.days = len(test_data)

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

    def fit(self):
        """Fit the continuous emission Gaussian HMM."""
        self._logger.info(">>> Extracting Features")
        observations = HMMStockPredictor._extract_features(self.train_data)
        self._logger.info("Features extraction Completed <<<")
        # Fit the HMM using the fit feature of hmmlearn
        self.hmm.fit(observations)

    def _compute_all_possible_outcomes(
        self, n_intervals_frac_change, n_intervals_frac_high, n_intervals_frac_low
    ):
        """Creates np arrays with evenly  spaced numbers for each range."""
        frac_change_range = np.linspace(-0.1, 0.1, n_intervals_frac_change)
        frac_high_range = np.linspace(0, 0.1, n_intervals_frac_high)
        frac_low_range = np.linspace(0, 0.1, n_intervals_frac_low)

        self._possible_outcomes = np.array(
            list(itertools.product(frac_change_range, frac_high_range, frac_low_range))
        )

    def _get_most_probable_outcome(self, day_index):
        """
        Using the fitted HMM, calculate the most probable outcome for a given day (e.g. prices will rise by 0.01).
        :param day_index: Current day index
        :return: The HMM's predicted movements in frac_change, frac_high, frac_low
        """
        # Use the previous n_latency_days worth of data for predictions
        previous_data_start_index = max(0, day_index - self.n_latency_days)
        previous_data_end_index = max(0, day_index - 1)
        previous_data = self.test_data.iloc[
            previous_data_start_index:previous_data_end_index
        ]
        previous_data_features = HMMStockPredictor._extract_features(previous_data)

        outcome_score = []

        # Score all possible outcomes and select the most probable one to use for prediction
        for possible_outcome in self._possible_outcomes:
            total_data = np.row_stack((previous_data_features, possible_outcome))
            outcome_score.append(self.hmm.score(total_data))

        # Get the index of the most probable outcome and return it
        most_probable_outcome = self._possible_outcomes[np.argmax(outcome_score)]

        return most_probable_outcome

    def predict_close_price(self, day_index):
        """Predict close price for a given day."""
        open_price = self.test_data.iloc[day_index]["Open"]
        (
            predicted_frac_change,
            pred_frac_high,
            pred_frac_low,
        ) = self._get_most_probable_outcome(day_index)
        return open_price * (1 + predicted_frac_change)

    def predict_close_prices_for_period(self):
        """
        Predict close prices for the testing period.
        :return: List object of predicted close prices
        """
        predicted_close_prices = []
        print(
            "Predicting Close prices from "
            + str(self.test_data.index[0])
            + " to "
            + str(self.test_data.index[-1])
        )
        for day_index in tqdm(range(self.days)):
            predicted_close_prices.append(self.predict_close_price(day_index))
        self.predicted_close = predicted_close_prices
        return predicted_close_prices

    def real_close_prices(self):
        """ "Store and return the actual close prices."""
        actual_close_prices = self.test_data.loc[:, ["Close"]]
        return actual_close_prices

    def add_future_days(self):
        """
        Add rows to the test data dataframe for the future days being predicted with accurate days. The rows are left
        with NaN values for now as they will be populated whilst predicting.
        """
        last_day = self.test_data.index[-1] + timedelta(days=self.days_in_future)

        # Create a new df with future days x days in the future based off the -f input. Concat the new df with
        # self.test_data.
        future_dates = pd.date_range(
            self.test_data.index[-1] + pd.offsets.DateOffset(1), last_day
        )
        second_df = pd.DataFrame(
            index=future_dates, columns=["High", "Low", "Open", "Close"]
        )
        self.test_data = pd.concat([self.test_data, second_df])

        # Replace the opening price for the first day in the future with the close price of the previous day
        self.test_data.iloc[self.days]["Open"] = self.test_data.iloc[self.days - 1][
            "Close"
        ]

    def predict_close_price_fut_days(self, day_index):
        """
        Predict the close prices for the days in the future beyond the available data and populate the DF accordingly.
        :param day_index - index in DF for  current day being predicted.
        :return: Predicted close price for given day.
        """
        open_price = self.test_data.iloc[day_index]["Open"]

        # Calculate the most likely fractional changes using the trained HMM
        (
            predicted_frac_change,
            pred_frac_high,
            pred_frac_low,
        ) = self._get_most_probable_outcome(day_index)
        predicted_close_price = open_price * (1 + predicted_frac_change)

        # Fill in the dataframe based on predictions
        self.test_data.iloc[day_index]["Close"] = predicted_close_price
        self.test_data.iloc[day_index]["High"] = open_price * (1 + pred_frac_high)
        self.test_data.iloc[day_index]["Low"] = open_price * (1 - pred_frac_low)

        return predicted_close_price

    def predict_close_prices_for_future(self):
        """
        Calls the "predict_close_price_fut_days" function for each day in the future to predict future close prices.
        """
        predicted_close_prices = []
        future_indices = len(self.test_data) - self.days_in_future
        print(
            "Predicting future Close prices from "
            + str(self.test_data.index[future_indices])
            + " to "
            + str(self.test_data.index[-1])
        )

        # Iterate over only the final x days in the test data dataframe.
        for day_index in tqdm(range(future_indices, len(self.test_data))):
            predicted_close_prices.append(self.predict_close_price_fut_days(day_index))
            # Replace the next days Opening price (which is currently NaN) with the previous days predicted close price
            try:
                self.test_data.iloc[day_index + 1]["Open"] = self.test_data.iloc[
                    day_index
                ]["Close"]
            except IndexError:
                continue

        # Return the predicted close prices
        self.predicted_close = predicted_close_prices

        return predicted_close_prices
