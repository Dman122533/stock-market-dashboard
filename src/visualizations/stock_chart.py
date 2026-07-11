import plotly.graph_objects as go


def create_price_chart(history, ticker):
    """
    Creates an interactive stock price chart.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history.index,
            y=history["Close"],
            mode="lines",
            name=ticker
        )
    )

    fig.update_layout(
        title=f"{ticker} Stock Price History",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        hovermode="x"
    )

    return fig