import pandas as pd
import yfinance as yf



def calculate_portfolio_history(positions, period="1y"):
    """
    Calculates historical portfolio value over time.
    """

    portfolio_history = pd.Series(dtype=float)


    for position in positions:

        ticker = position["ticker"]
        shares = position["shares"]


        stock_history = yf.download(
            ticker,
            period=period,
            auto_adjust=True
        )


        prices = stock_history["Close"].squeeze()


        position_value = prices * shares


        if portfolio_history.empty:

            portfolio_history = position_value

        else:

            portfolio_history = (
                portfolio_history.add(
                    position_value,
                    fill_value=0
                )
            )

    print(portfolio_history)
    return portfolio_history