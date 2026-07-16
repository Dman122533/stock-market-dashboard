import yfinance as yf


def get_stock_data(ticker_symbol):
    """
    Retrieves stock/ETF information from Yahoo Finance.

    Parameters:
        ticker_symbol (str): Stock ticker symbol (ex: AAPL)

    Returns:
        dict: Asset information
    """

    stock = yf.Ticker(ticker_symbol)
    info = stock.info

    return {
        "name": (
            info.get("longName")
            or info.get("shortName")
            or ticker_symbol.upper()
        ),

        "price": (
            info.get("currentPrice")
            or info.get("regularMarketPrice")
        ),

        "previous_close": info.get("previousClose"),

        "market_cap": info.get("marketCap"),

        "sector": (
            info.get("sector")
            or info.get("category")
            or "N/A"
        ),

        "52_week_high": info.get("fiftyTwoWeekHigh"),

        "52_week_low": info.get("fiftyTwoWeekLow"),

        "asset_type": (
            info.get("quoteType", "EQUITY")
            or "N/A"
        )
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