import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils.helpers import format_market_cap
from src.api.stock_api import get_stock_data, get_stock_history
from src.visualizations.stock_chart import create_price_chart, create_volume_chart
from src.analytics.stock_metrics import calculate_total_return, calculate_volatility, calculate_moving_averages, calculate_average_volume, calculate_latest_volume_change
from src.analytics.risk_metrics import calculate_sharpe_ratio, calculate_max_drawdown, calculate_beta
from src.portfolio.portfolio import calculate_portfolio_value, calculate_allocation


st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)


st.title("📈 Stock Market Dashboard")
dashboard_tab, portfolio_tab = st.tabs(
    [
        "Stock Dashboard",
        "Portfolio Tracker"
    ]
)
with dashboard_tab:
    if "ticker" not in st.session_state:
        st.session_state.ticker = None

    ticker = st.text_input(
        "Enter stock ticker",
        "AAPL"
    )


    if st.button("Search"):

        st.session_state.ticker = ticker
    if st.session_state.ticker:

        ticker = st.session_state.ticker

        stock = get_stock_data(ticker)
        st.subheader(stock["name"])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Current Price",
                f"${stock['price']:,.2f}"
            )

        with col2:
            st.metric(
                "Previous Close",
                f"${stock['previous_close']:,.2f}"
            )

        with col3:
            st.metric(
                "Market Cap",
                format_market_cap(stock["market_cap"])
            )


        col4, col5 = st.columns(2)

        with col4:
            st.metric(
                "52 Week High",
                f"${stock['52_week_high']:,.2f}"
            )

        with col5:
            st.metric(
                "52 Week Low",
                f"${stock['52_week_low']:,.2f}"
            )
        st.subheader("Price History")

        period = st.selectbox(
        "Select Time Period",
        [
            "1mo",
            "6mo",
            "1y",
            "5y"
        ]
        )

        history = get_stock_history(
            ticker,
            period
        )
        history = calculate_moving_averages(history)
        chart = create_price_chart(
            history,
            ticker
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )
        st.subheader("Trading Volume")

        volume_chart = create_volume_chart(
            history,
            ticker
        )

        st.plotly_chart(
            volume_chart,
            use_container_width=True
        )
        st.subheader("Performance Metrics")
        total_return = calculate_total_return(history)

        volatility = calculate_volatility(history)


        col1, col2 = st.columns(2)


        with col1:
            st.metric(
                "Total Return",
                f"{total_return:.2%}"
            )


        with col2:
            st.metric(
                "Volatility",
                f"{volatility:.2%}"
            )
        st.subheader("Risk Metrics")
        
        sharpe = calculate_sharpe_ratio(history)

        drawdown = calculate_max_drawdown(history)


        col8, col9 = st.columns(2)


        with col8:
            st.metric(
                "Sharpe Ratio",
                f"{sharpe:.2f}"
            )


        with col9:
            st.metric(
                "Maximum Drawdown",
                f"{drawdown:.2%}"
            )
        market_history = get_stock_history(
        "^GSPC",
        period
    )


        beta = calculate_beta(
            history,
            market_history
        )
        st.metric(
            "Beta vs S&P 500",
            f"{beta:.2f}"
        )
        st.subheader("Trading Activity")


        average_volume = calculate_average_volume(history)

        volume_change = calculate_latest_volume_change(history)


        col6, col7 = st.columns(2)


        with col6:
            st.metric(
                "Average Volume",
                f"{average_volume / 1_000_000:.2f}M"
            )


        with col7:
            st.metric(
                "Volume Change",
                f"{volume_change:.2%}"
            )
with portfolio_tab:
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = []
    st.header("💼 Portfolio Tracker")

    st.write(
        "Enter your stock holdings below."
    )
    ticker_input = st.text_input(
    "Stock ticker",
    "AAPL"
    )


    shares_input = st.number_input(
        "Number of shares",
        min_value=0.0,
        value=1.0
    )
    if st.button("Add Holding"):

        ticker = ticker_input.upper()

        price_data = get_stock_data(ticker)

        existing_holding = None

        for holding in st.session_state.portfolio:

            if holding["ticker"] == ticker:

                existing_holding = holding
                break

        if existing_holding:

            existing_holding["shares"] += shares_input
            existing_holding["price"] = price_data["price"]

        else:

            st.session_state.portfolio.append(
                {
                    "ticker": ticker,
                    "shares": shares_input,
                    "price": price_data["price"]
                }
            )
    st.subheader("Current Holdings")


    portfolio_rows = []

    total_value = calculate_portfolio_value(
        st.session_state.portfolio
    )

    for holding in st.session_state.portfolio:

        position_value = (
            holding["shares"]
            * holding["price"]
        )

        allocation = (
            position_value / total_value
        ) if total_value > 0 else 0

        portfolio_rows.append(
            {
                "Ticker": holding["ticker"],
                "Shares": holding["shares"],
                "Current Price": holding["price"],
                "Position Value": position_value,
                "Allocation": allocation
            }
        )
    portfolio_df = pd.DataFrame(
        portfolio_rows
    )
    if not portfolio_df.empty:

        display_df = portfolio_df.copy()

        display_df["Current Price"] = (
            display_df["Current Price"]
            .map(lambda x: f"${x:,.2f}")
        )

        display_df["Position Value"] = (
            display_df["Position Value"]
            .map(lambda x: f"${x:,.2f}")
        )

        display_df["Allocation"] = (
            display_df["Allocation"]
            .map(lambda x: f"{x:.1%}")
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Add a stock holding to view your portfolio.")
    if st.session_state.portfolio:

        st.subheader("Portfolio Summary")

        total_value = calculate_portfolio_value(
            st.session_state.portfolio
        )

        st.metric(
            "Total Portfolio Value",
            f"${total_value:,.2f}"
        )

        allocation = calculate_allocation(
            st.session_state.portfolio
        )

        allocation_df = pd.DataFrame(
            {
                "Ticker": allocation.keys(),
                "Allocation": allocation.values()
            }
        )

        fig = px.pie(
            allocation_df,
            names="Ticker",
            values="Allocation",
            title="Portfolio Allocation"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )