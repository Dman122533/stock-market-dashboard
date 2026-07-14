import streamlit as st
from tabs.stock_tab import show_stock_tab
from tabs.portfolio_tab import show_portfolio_tab
from tabs.analytics_tab import show_analytics_tab
from database.database import create_tables

st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)
create_tables()


st.title("📈 Stock Market Dashboard")
dashboard_tab, portfolio_tab, analytics_tab = st.tabs(
    [
        "Stock Dashboard",
        "Portfolio Tracker",
        "Analytics"
    ]
)
with dashboard_tab:
    show_stock_tab()
with portfolio_tab:
    show_portfolio_tab()
with analytics_tab:
    show_analytics_tab()