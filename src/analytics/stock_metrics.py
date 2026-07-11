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
def calculate_moving_averages(history):
    """
    Calculates 20-day and 50-day moving averages.
    """

    history["MA20"] = (
        history["Close"]
        .rolling(window=20)
        .mean()
    )

    history["MA50"] = (
        history["Close"]
        .rolling(window=50)
        .mean()
    )

    return history
def calculate_average_volume(history):
    """
    Calculates average daily trading volume.
    """

    average_volume = history["Volume"].mean()

    return average_volume



def calculate_latest_volume_change(history):
    """
    Calculates the percentage change in volume
    from the previous trading day.
    """

    latest_volume = history["Volume"].iloc[-1]
    previous_volume = history["Volume"].iloc[-2]

    change = (
        (latest_volume - previous_volume)
        / previous_volume
    )

    return change