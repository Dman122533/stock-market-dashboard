import streamlit as st
from src.utils.helpers import format_market_cap
from src.api.stock_api import get_stock_data


st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)


st.title("📈 Stock Market Dashboard")


ticker = st.text_input(
    "Enter stock ticker",
    "AAPL"
)


if st.button("Search"):

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