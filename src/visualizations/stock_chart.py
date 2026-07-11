import plotly.graph_objects as go


def create_price_chart(history, ticker):

    fig = go.Figure()


    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=history.index,
            open=history["Open"],
            high=history["High"],
            low=history["Low"],
            close=history["Close"],
            name=ticker
        )
    )


    # 20 day moving average
    fig.add_trace(
        go.Scatter(
            x=history.index,
            y=history["MA20"],
            mode="lines",
            name="20 Day MA"
        )
    )


    # 50 day moving average
    fig.add_trace(
        go.Scatter(
            x=history.index,
            y=history["MA50"],
            mode="lines",
            name="50 Day MA"
        )
    )


    fig.update_layout(
        title=f"{ticker} Price History",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        xaxis_rangeslider_visible=False
    )


    return fig