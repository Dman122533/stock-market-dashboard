import pandas as pd
import yfinance as yf



def calculate_portfolio_history(positions, period="1y"):
    """
    Calculates historical portfolio value over time.
    """

    portfolio_history = None


    for position in positions:

        ticker = position["ticker"]
        shares = position["shares"]


        stock_history = yf.download(
            ticker,
            period=period,
            auto_adjust=True
        )


        prices = stock_history["Close"]


        position_value = prices * shares


        if portfolio_history is None:

            portfolio_history = position_value

        else:

            portfolio_history = (
                portfolio_history
                .add(
                    position_value,
                    fill_value=0
                )
            )


    return portfolio_history