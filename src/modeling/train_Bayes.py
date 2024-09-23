"""
This file contains functions for training a Bayesian model
Note 1: Attempting to use this concept in stocks prediction (performing / not performing)

Formula: P(A|B) = P(B|A) * P(A) / P(B)
P(Stock A performing | Stock B performing) = P(Stock B performing | Stock A performing) * P(Stock A performing) / P(Stock B performing)
P(Stock B performing) can be computed by looking at the price history of Stock B,
    and compute daily percentage change in price. If the percentage change is positive, we consider it as "performing", otherwise "not performing".
P(Stock A performing) can be computed in the same way.
P(Stock B performing | Stock A performing) can be computed by looking at the percentage change in price of Stock B on the days when Stock A is performing.
"""

import dataset as ds
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def p_stock_performing(ticker, price_type="Close"):
    """
    Compute the probability of Stock A performing based on the price data.

    Args:
        ticker (str): The stock ticker symbol.
        price_type (str): The type of price data to use. Default is "Close".

    Returns:
        float: The probability of Stock A performing.
    """

    price_data = ds.get_price_all_time(ticker, price_type)

    price_data["Daily_Return"] = price_data["Close"].pct_change()
    price_data["Performing"] = price_data["Daily_Return"] > 0
    prob_performing = price_data.iloc[1:]["Performing"].mean()
    return prob_performing


def p_conditional(tickerA, tickerB, threshold=0):
    """
    Compute the conditional probability of Stock A performing given the other is performing.

    Args:
        tickerA (str): The stock ticker symbol for Stock A.
        tickerB (str): The stock ticker symbol for Stock B.
        threshold (float): The threshold for considering a stock as performing. Default is 0.

    Returns:
        float: The conditional probability of Stock A performing given the other is performing.
    """
    price_data_A = ds.get_price_all_time(tickerA, "Close")
    price_data_B = ds.get_price_all_time(tickerB, "Close")

    start_date = max(price_data_A.index.min(), price_data_B.index.min())
    last_date = min(price_data_A.index.max(), price_data_B.index.max())

    price_data_A = price_data_A.loc[start_date + pd.Timedelta(days=1) :]
    price_data_B = price_data_B.loc[start_date : last_date - pd.Timedelta(days=1)]

    price_data_A["Daily_Return"] = price_data_A["Close"].pct_change()
    price_data_A["Performing"] = price_data_A["Daily_Return"] > threshold

    price_data_B["Daily_Return"] = price_data_B["Close"].pct_change()
    price_data_B["Performing"] = price_data_B["Daily_Return"] > 0

    price_data_A.reset_index(drop=False, inplace=True)
    price_data_B.reset_index(drop=False, inplace=True)

    A_when_B_performs = price_data_A[price_data_B["Performing"]]
    prob_A_performs_given_B = A_when_B_performs["Performing"].mean()
    return prob_A_performs_given_B


def bayes_theorem(tickerA, tickerB):
    """
    Compute the probability of Stock A performing given Stock B is performing.

    Args:
        tickerA (str): The stock ticker symbol for Stock A.
        tickerB (str): The stock ticker symbol for Stock B.

    Returns:
        float: The probability of Stock A performing given Stock B is performing.
    """

    prob_A = p_stock_performing(tickerA)
    prob_B = p_stock_performing(tickerB)
    prob_A_given_B = p_conditional(tickerA, tickerB)

    prob_B_given_A = prob_A_given_B * prob_A / prob_B
    return prob_A_given_B


def get_conditional_performance_graph(
    tickerA, tickerB, threshold_list=list(np.arange(0, 0.06, 0.01))
):
    """
    Generates and plots a graph showing the conditional performance probability of tickerA
    given the performance of tickerB the previous day.

    Args:
        tickerA (str): The ticker symbol of the first stock.
        tickerB (str): The ticker symbol of the second stock.
        threshold_list (list, optional): A list of performance thresholds to evaluate.
                                         Defaults to a list of values from 0 to 0.05 with a step of 0.01.

    Returns:
        None
    """

    performance_prob = []
    print(
        f"Getting probability of {tickerA} performing given {tickerB} performed the day before...."
    )
    for threshold in threshold_list:
        performance_prob.append(p_conditional(tickerA, tickerB, threshold))

    # plot the graph
    plt.plot(threshold_list, performance_prob)
    plt.xlabel("Performance Threshold")
    plt.ylabel("Probability")
    plt.show()
