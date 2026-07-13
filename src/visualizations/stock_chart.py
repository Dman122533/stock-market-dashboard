import plotly.graph_objects as go
from src.visualizations.chart_theme import apply_chart_theme


def create_price_chart(history, ticker):

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=history.index,
            open=history["Open"],
            high=history["High"],
            low=history["Low"],
            close=history["Close"],
            name=ticker,
            increasing_line_color="#00cc96",
            decreasing_line_color="#ef553b"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history.index,
            y=history["MA20"],
            mode="lines",
            name="20-Day Moving Average"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history.index,
            y=history["MA50"],
            mode="lines",
            name="50-Day Moving Average"
        )
    )

    fig.update_layout(
        title=f"📈 {ticker} Price History",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        xaxis_rangeslider_visible=False
    )

    fig = apply_chart_theme(fig)

    return fig


def create_volume_chart(history, ticker):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=history.index,
            y=history["Volume"],
            name="Volume",
            opacity=0.7
        )
    )

    fig.update_layout(
        title=f"📊 {ticker} Trading Volume",
        xaxis_title="Date",
        yaxis_title="Shares Traded"
    )

    fig = apply_chart_theme(fig)

    return fig