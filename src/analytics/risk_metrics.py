import yfinance as yf
import pandas as pd


def calculate_returns(history):
    """
    Calculates daily percentage returns.
    """

    returns = history["Close"].pct_change()

    return returns



def calculate_sharpe_ratio(history, risk_free_rate=0.04):
    """
    Calculates annualized Sharpe Ratio.

    Assumes 252 trading days/year.
    """

    returns = calculate_returns(history)

    excess_returns = (
        returns - risk_free_rate / 252
    )

    sharpe = (
        excess_returns.mean()
        /
        excess_returns.std()
    ) * (252 ** 0.5)

    return sharpe



def calculate_max_drawdown(history):
    """
    Calculates the largest historical drop
    from a peak price.
    """

    prices = history["Close"]

    rolling_max = prices.cummax()

    drawdown = (
        prices - rolling_max
    ) / rolling_max

    max_drawdown = drawdown.min()

    return max_drawdown



def calculate_beta(stock_history, market_history):
    """
    Calculates beta relative to market.

    Uses S&P 500 (^GSPC) as benchmark.
    """

    stock_returns = calculate_returns(stock_history)

    market_returns = calculate_returns(market_history)


    combined = pd.concat(
        [
            stock_returns,
            market_returns
        ],
        axis=1
    ).dropna()


    covariance = combined.iloc[:,0].cov(
        combined.iloc[:,1]
    )

    market_variance = combined.iloc[:,1].var()


    beta = covariance / market_variance

    return beta