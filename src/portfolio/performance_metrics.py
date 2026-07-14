import pandas as pd
import numpy as np



def calculate_total_return(history):
    """
    Calculates total portfolio return.
    """

    starting_value = history.iloc[0]

    ending_value = history.iloc[-1]

    total_return = (
        ending_value - starting_value
    ) / starting_value

    return total_return



def calculate_daily_returns(history):
    """
    Calculates daily percentage returns.
    """

    daily_returns = history.pct_change()

    return daily_returns.dropna()



def calculate_volatility(history):
    """
    Calculates annualized volatility.
    """

    daily_returns = calculate_daily_returns(
        history
    )

    volatility = (
        daily_returns.std()
        *
        np.sqrt(252)
    )

    return volatility



def calculate_sharpe_ratio(
    history,
    risk_free_rate=0.04
):
    """
    Calculates annualized Sharpe ratio.
    """

    daily_returns = calculate_daily_returns(
        history
    )

    if daily_returns.empty:
        return 0

    daily_risk_free_rate = (
        risk_free_rate / 252
    )

    excess_returns = (
        daily_returns
        -
        daily_risk_free_rate
    )

    average_return = (
        excess_returns.mean()
        *
        252
    )

    volatility = (
        daily_returns.std()
        *
        np.sqrt(252)
    )

    if volatility == 0 or pd.isna(volatility):
        return 0

    sharpe_ratio = (
        average_return
        /
        volatility
    )

    return sharpe_ratio