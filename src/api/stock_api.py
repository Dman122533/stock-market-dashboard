import yfinance as yf


def get_stock_data(ticker_symbol):
    """
    Retrieves stock information from Yahoo Finance.

    Parameters:
        ticker_symbol (str): Stock ticker symbol (ex: AAPL)

    Returns:
        dict: Stock information
    """
    stock = yf.Ticker(ticker_symbol)
    info = stock.info

    return {
        "name": info.get("longName"),
        "price": info.get("currentPrice", info.get("regularMarketPrice")),
        "previous_close": info.get("previousClose"),
        "market_cap": info.get("marketCap"),
        "sector": info.get("sector"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow")
    }

def get_stock_history(ticker_symbol, period="1y"):
    """
    Retrieves historical stock price data.

    Parameters:
        ticker_symbol (str): Stock ticker symbol
        period (str): Time period for historical data

    Returns:
        DataFrame: Historical stock prices
    """

    stock = yf.Ticker(ticker_symbol)

    history = stock.history(period=period)

    return history