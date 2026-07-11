import pandas as pd


def calculate_daily_returns(history):
    """
    Calculates daily percentage returns.
    """

    returns = history["Close"].pct_change()

    return returns



def calculate_total_return(history):
    """
    Calculates total return over selected period.
    """

    start_price = history["Close"].iloc[0]
    end_price = history["Close"].iloc[-1]

    total_return = (
        (end_price - start_price)
        / start_price
    )

    return total_return



def calculate_volatility(history):
    """
    Calculates annualized volatility.
    """

    returns = calculate_daily_returns(history)

    volatility = returns.std() * (252 ** 0.5)

    return volatility