# Dependencies
## !pip install yfinance

# Import Statements
import yfinance as yf
import requests


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

        resulting_dict = {}
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
