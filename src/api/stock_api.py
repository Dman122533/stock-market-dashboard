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
        "price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "sector": info.get("sector"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow")
    }