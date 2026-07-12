import pandas as pd


def calculate_max_drawdown(history):
    """
    Calculates the largest percentage drop
    from a previous portfolio peak.
    """

    rolling_peak = history.cummax()

    drawdown = (
        history - rolling_peak
    ) / rolling_peak

    return drawdown.min()



def calculate_best_day(history):
    """
    Calculates the best daily return.
    """

    daily_returns = history.pct_change()

    return daily_returns.max()



def calculate_worst_day(history):
    """
    Calculates the worst daily return.
    """

    daily_returns = history.pct_change()

    return daily_returns.min()