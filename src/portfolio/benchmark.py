import yfinance as yf



def get_benchmark_history(period="1y"):
    """
    Retrieves S&P 500 historical data.
    """

    sp500 = yf.download(
        "^GSPC",
        period=period,
        auto_adjust=True
    )


    benchmark_history = (
        sp500["Close"]
        .squeeze()
    )


    return benchmark_history
import yfinance as yf


def get_benchmark_history(period="1y"):

    sp500 = yf.download(
        "^GSPC",
        period=period,
        auto_adjust=True
    )

    benchmark_history = (
        sp500["Close"]
        .squeeze()
    )

    return benchmark_history



def normalize_series(series):

    return (
        series / series.iloc[0]
    ) * 100

def calculate_benchmark_return(history):
    """
    Calculates benchmark total return.
    """

    starting_value = history.iloc[0]

    ending_value = history.iloc[-1]


    return (
        ending_value - starting_value
    ) / starting_value