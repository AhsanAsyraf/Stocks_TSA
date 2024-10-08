# Dependencies
## !pip install yfinance

# Import Statements
import yfinance as yf
import requests
import os
import pandas as pd


# Helper Functions
def get_fundamentals(ticker):
    """
    Retrieve fundamental financial metrics for a specified stock ticker.

    This function fetches and returns a dictionary of fundamental financial data
    for the given stock ticker using the Yahoo Finance API. The returned dictionary
    includes key metrics that are often used to evaluate a company's financial health,
    such as market capitalization, enterprise value, profit margins, and more.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple, 'MSFT' for Microsoft).

    Returns:
        dict: A dictionary where the keys are fundamental metric names (e.g., 'marketCap',
              'enterpriseValue') and the values are the corresponding data points.
              If a metric is unavailable for a specific company, the value will be None.

    Raises:
        ValueError: If no data is found for the given ticker.
        KeyError: If the ticker symbol is invalid or not found.
        Exception: For any other unexpected errors during the data retrieval process.

    Example:
        >>> get_fundamentals("AAPL")
        {
            'marketCap': 2250000000000,
            'enterpriseValue': 2300000000000,
            'priceToBook': 35.67,
            'trailingPE': 28.56,
            ...
        }
    """

    try:
        company_info = yf.Ticker(ticker).info

        resulting_dict = {"ticker": ticker}
        fundamental_metrics = [
            "marketCap",
            "enterpriseValue",
            "priceToSalesTrailing12Months",
            "priceToBook",
            "trailingPE",
            "forwardPE",
            "profitMargins",
            "returnOnAssets",
            "returnOnEquity",
            "earningsQuarterlyGrowth",
            "totalRevenue",
            "revenueGrowth",
            "freeCashflow",
            "totalDebt",
            "debtToEquity",
            "trailingEps",
            "forwardEps",
            "pegRatio",
            "dividendRate",
            "dividendYield",
            "payoutRatio",
        ]

        for metric in fundamental_metrics:
            resulting_dict[metric] = company_info.get(metric, None)

        return resulting_dict

    except ValueError as ve:
        print(ve)
    except KeyError as ke:
        print(ke)
        print(f"The ticker you entered '{ticker}' does not exist or was not found.")
    except Exception as ex:
        print(f"An error occurred: {ex}")


def get_Nasdaq_ticker_list(
    file_path=os.path.join("..", "data", "raw", "nasdaq_screener.csv"),
):
    """
    Retrieve a list of tickers from a NASDAQ company file.

    Args:
        file_path (string): The path to the NASDAQ screener CSV file. Defaults to os.path.join("..", "data", "raw", "nasdaq_screener.csv").

    Returns:
        list: A list of tickers for all NASDAQ stocks. Returns an empty list if an error occurs.

    Raises:
        FileNotFoundError: If the CSV file is not found at the specified path.
        KeyError: If the 'Symbol' column is not present in the CSV file.
        Exception: For any other unexpected errors during file reading or processing.
    """
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return []

        raw_nasdaq_data = pd.read_csv(file_path)

        if "Symbol" not in raw_nasdaq_data.columns:
            print("Error: 'Symbol' column not found in the file.")
            return []

        ticker_list = list(raw_nasdaq_data["Symbol"].dropna().unique())
        return ticker_list

    except (FileNotFoundError, KeyError) as e:
        print(e)
        return []

    except Exception as e:
        print(f"Error encountered: {e}")


def get_price_1year(ticker, price_type="All"):
    """
    Retrieve price data for the given stock ticker for the past year.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple, 'MSFT' for Microsoft).
        price_type (str): The type of price data to retrieve. Options are 'All', 'Open', 'Close',
                          'High', 'Low' (e.g. 'Close' means Closing Price ONLY). Defaults to 'All'.

    Returns:
        pd.DataFrame or pd.Series: Price data for the provided ticker, based on the specified price_type.
                                   If 'All' is selected, it returns the full price DataFrame. Otherwise, it returns the selected column.

    Raises:
        ValueError: If the `price_type` is not a valid option.
    """

    try:
        symbol = yf.Ticker(ticker)
        price_df = symbol.history(period="1y")

        valid_price_types = {
            "All": price_df,
            "Open": price_df["Open"],
            "Close": price_df["Close"],
            "High": price_df["High"],
            "Low": price_df["Low"],
        }

        if price_type not in valid_price_types:
            raise ValueError(
                f"Invalid price_type: {price_type}. Choose from 'All', 'Open', 'Close', 'High', 'Low'."
            )

        return valid_price_types[price_type]

    except ValueError as ve:
        print(ve)
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_price_all_time(ticker, price_type="All"):
    """
    Retrieve price data for the given stock ticker for all available time.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple, 'MSFT' for Microsoft).
        price_type (str): The type of price data to retrieve. Options are 'All', 'Open', 'Close',
                          'High', 'Low' (e.g. 'Close' means Closing Price ONLY). Defaults to 'All'.

    Returns:
        pd.DataFrame: Price data for the provided ticker. If 'All' is selected, it returns the full price DataFrame.
                        Otherwise, it returns the selected column.
    Raises:
        ValueError: If the `price_type` is not a valid option.
    """

    try:
        symbol = yf.Ticker(ticker)
        price_df = symbol.history(period="max")

        valid_price_types = {
            "All": price_df,
            "Open": price_df["Open"].to_frame(),
            "Close": price_df["Close"].to_frame(),
            "High": price_df["High"].to_frame(),
            "Low": price_df["Low"].to_frame(),
        }

        if price_type not in valid_price_types:
            raise ValueError(
                f"Invalid price_type: {price_type}. Choose from 'All', 'Open', 'Close', 'High', 'Low'."
            )

        return valid_price_types[price_type]

    except ValueError as ve:
        print(ve)
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
