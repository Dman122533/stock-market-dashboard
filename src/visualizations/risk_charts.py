import plotly.express as px


def create_drawdown_chart(history):
    """
    Creates portfolio drawdown chart.
    """

    rolling_peak = history.cummax()

    drawdown = (
        (history - rolling_peak)
        /
        rolling_peak
    )

    fig = px.line(
        drawdown,
        title="Portfolio Drawdown"
    )

    fig.update_yaxes(
        tickformat=".2%"
    )

    return fig



def create_returns_distribution(history):
    """
    Creates daily return histogram.
    """

    daily_returns = history.pct_change()

    fig = px.histogram(
        daily_returns.dropna(),
        title="Daily Returns Distribution",
        nbins=30
    )

    fig.update_xaxes(
        tickformat=".2%"
    )

    return fig