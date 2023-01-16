import os
import sys
import argparse

from tatu_re.model.hmm import HMMStockPredictor
from tatu_re.model.utils import calc_mse, plot_results

def use_stock_predictor(company_name, start, end, future, metrics, plot, out_dir):
    # Correct incorrect inputs. Inputs should be of the form XXXX, but handle cases when users input 'XXXX'
    company_name = company_name.strip("'").strip('"')
    print(
        "Using continuous Hidden Markov Models to predict stock prices for "
        + str(company_name)
    )

    # Initialise HMMStockPredictor object and fit the HMM
    stock_predictor = HMMStockPredictor(
        company=company_name, start_date=start, end_date=end, future_days=future
    )
    print(
        "Training data period is from "
        + str(stock_predictor.train_data.index[0])
        + " to "
        + str(stock_predictor.train_data.index[-1])
    )
    stock_predictor.fit()

    # Get the predicted and actual stock prices and create a DF for saving if you'd like to get a metric for the model
    if metrics:
        predicted_close = stock_predictor.predict_close_prices_for_period()
        actual_close = stock_predictor.real_close_prices()
        actual_close["Predicted_Close"] = predicted_close
        output_df = actual_close.rename(columns={"Close": "Actual_Close"})

        # Calculate Mean Squared Error and save
        mse = calc_mse(output_df)
        out_name = f"{out_dir}/{company_name}_HMM_Prediction_{str(round(mse, 6))}.xlsx"
        output_df.to_excel(out_name)  # Requires openpyxl installed
        print(
            "All predictions saved. The Mean Squared Error for the "
            + str(stock_predictor.days)
            + " days considered is: "
            + str(mse)
        )

        # Plot and save results if plot is True
        if plot:
            plot_results(output_df, out_dir, company_name)

    # Predict for x days into the future
    if future:
        stock_predictor.add_future_days()
        future_pred_close = stock_predictor.predict_close_prices_for_future()

        print(
            "The predicted stock prices for the next "
            + str(future)
            + " days from "
            + str(stock_predictor.end_date)
            + " are: ",
            future_pred_close,
        )

        out_final = (
            f"{out_dir}/{company_name}_HMM_Predictions_{future}_days_in_future.xlsx"
        )
        stock_predictor.test_data.to_excel(out_final)  # Requires openpyxl installed
        print(
            "The full set of predictions has been saved, including the High, Low, Open and Close prices for "
            + str(future)
            + " days in the future."
        )


def main():
    # Set up arg_parser to handle inputs
    arg_parser = argparse.ArgumentParser()

    # Parse console inputs
    arg_parser.add_argument(
        "-n",
        "--stock_name",
        required=True,
        type=str,
        help="Takes in the name of a stock in the form XXXX e.g. AAPL. 'AAPL' will fail.",
    )
    arg_parser.add_argument(
        "-s",
        "--start_date",
        required=True,
        type=str,
        help="Takes in the start date of the time period being evaluated. Please input dates in the"
        "following way: 'year-month-day'",
    )
    arg_parser.add_argument(
        "-e",
        "--end_date",
        required=True,
        type=str,
        help="Takes in the end date of the time period being evaluated. Please input dates in the"
        "following way: 'year-month-day'",
    )
    arg_parser.add_argument(
        "-o",
        "--out_dir",
        type=str,
        default=None,
        help="Directory to save the CSV file that contains the actual stock prices along with the "
        "predictions for a given day.",
    )
    arg_parser.add_argument(
        "-p",
        "--plot",
        type=check_bool,
        nargs="?",
        const=True,
        default=False,
        help="Optional: Boolean flag specifying if the results should be plotted or not.",
    )
    arg_parser.add_argument(
        "-f",
        "--future",
        type=int,
        default=None,
        help="Optional: Value specifying how far in the future the user would like predictions.",
    )
    arg_parser.add_argument(
        "-m",
        "--metrics",
        type=check_bool,
        nargs="?",
        const=True,
        default=False,
        help="Optional: Boolean flag specifying that the user would like to see how accurate the "
        "model is at predicting prices in the testing dataset for which real data exists, i.e. "
        "dates before -e. This slows down prediction as all test days will have their close "
        "prices predicted, as opposed to just the future days, but provides a metric to score "
        "the HMM (Mean Squared Error). ",
    )
    args = arg_parser.parse_args()

    # Set variables from arguments
    company_name = args.stock_name
    start = args.start_date
    end = args.end_date
    future = args.future
    metrics = args.metrics
    plot = args.plot

    # Handle empty input case
    if not metrics and future is None:
        print(
            "No outputs selected as both historical predictions and future predictions are empty/None. Please repeat "
            "your inputs with a boolean value for -m, or an integer value for -f, or both."
        )
        sys.exit()

    # Use the current working directory for saving if there is no input
    if args.out_dir is None:
        out_dir = os.getcwd()
    else:
        out_dir = args.out_dir

    use_stock_predictor(company_name, start, end, future, metrics, plot, out_dir)


if __name__ == "__main__":
    # Model prediction scoring is saved in the same directory as the images that are tested.
    main()
    