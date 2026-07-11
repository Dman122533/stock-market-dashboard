import streamlit as st

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
            stock["price"]
        )

    with col2:
        st.metric(
            "Sector",
            stock["sector"]
        )

    with col3:
        st.metric(
            "Market Cap",
            stock["market_cap"]
        )