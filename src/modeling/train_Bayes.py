"""
This file contains functions for training an empirical model based on conditional probability concept.
Note 1: Attempting to use this concept in stocks prediction (performing / not performing)

Bayesian probability is not applicable in this case because events are:
   Event A: Stock A performing today
   Event B: Stock B performed yesterday
P(A|B) is possible, but P(B|A) is not possible because the logic is not there.
"""

import dataset as ds
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
