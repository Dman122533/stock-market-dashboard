import streamlit as st
import pandas as pd
import plotly.express as px

from src.portfolio.portfolio import calculate_portfolio_value, calculate_allocation, refresh_portfolio_prices
from src.portfolio.portfolio_metrics import get_number_of_holdings, get_largest_position, get_average_position_size
from src.portfolio.sector_analysis import calculate_sector_allocation
from src.visualizations.chart_theme import apply_chart_theme
from src.portfolio.portfolio_performance import calculate_portfolio_history
from src.portfolio.performance_metrics import calculate_total_return, calculate_volatility, calculate_sharpe_ratio
from src.portfolio.benchmark import get_benchmark_history, normalize_series, calculate_benchmark_return
from src.portfolio.risk_metrics import calculate_max_drawdown, calculate_best_day, calculate_worst_day
from src.visualizations.risk_charts import create_drawdown_chart, create_returns_distribution
from src.api.stock_api import get_stock_data, get_stock_history

def show_portfolio_tab():
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = []
    st.header("💼 Portfolio Dashboard")

    st.subheader("📈 Portfolio Overview")
    st.divider()
    if st.session_state.portfolio:

        total_value = calculate_portfolio_value(
            st.session_state.portfolio
        )

        holdings_count = get_number_of_holdings(
            st.session_state.portfolio
        )

        largest_position = get_largest_position(
            st.session_state.portfolio
        )

        average_position = get_average_position_size(
            st.session_state.portfolio
        )


        col1, col2, col3, col4 = st.columns(4)


        with col1:
            st.metric(
                "💰 Portfolio Value",
                f"${total_value:,.2f}"
            )


        with col2:
            st.metric(
                "📊 Holdings",
                holdings_count
            )


        with col3:
            st.metric(
                "📈 Largest Position",
                largest_position
            )


        with col4:
            st.metric(
                "📌 Avg Position",
                f"${average_position:,.2f}"
            )
        
    else:

        st.info(
            "Add holdings to view portfolio statistics."
        )
    
    st.divider()
    if st.session_state.portfolio:

        st.subheader("📊 Portfolio Breakdown")

        col1, col2 = st.columns(2)

        with col1:

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
                title="Portfolio Allocation",
            )
            fig = apply_chart_theme(fig)
            fig.update_traces(
                            hovertemplate="%{label}<br>%{percent}"
                        )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
            

        with col2:

            sector_allocation = calculate_sector_allocation(
                st.session_state.portfolio
            )


            sector_df = pd.DataFrame(
                {
                    "Sector": sector_allocation.keys(),
                    "Allocation": sector_allocation.values()
                }
            )


            sector_fig = px.pie(
                sector_df,
                names="Sector",
                values="Allocation",
                title="Sector Allocation",
            )
            sector_fig = apply_chart_theme(sector_fig)
            sector_fig.update_traces(
                        hovertemplate="%{label}<br>%{percent}"
                    )
            st.plotly_chart(
                sector_fig,
                use_container_width=True
            )
            
    st.divider()
    
    st.subheader("📋 Current Holdings")


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
                "Shares": round(holding["shares"], 2),
                "Price": holding["price"],
                "Value": position_value,
                "Allocation": allocation
            }
        )
    portfolio_df = pd.DataFrame(
        portfolio_rows
    )
    
    if not portfolio_df.empty:

        display_df = portfolio_df.copy()

        display_df["Price"] = (
            display_df["Price"]
            .map(lambda x: f"${x:,.2f}")
        )

        display_df["Value"] = (
            display_df["Value"]
            .map(lambda x: f"${x:,.2f}")
        )

        display_df["Allocation"] = (
            display_df["Allocation"] * 100
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Ticker": st.column_config.TextColumn(
                    "Ticker"
                ),
                "Shares": st.column_config.NumberColumn(
                    "Shares",
                    format="%.2f"
                ),
                "Allocation": st.column_config.ProgressColumn(
                    "Allocation",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100
                )
            }
        )

    else:

        st.info("Add a stock holding to view your portfolio.")
    
    st.divider()
    with st.expander("⚙️ Manage Portfolio", expanded=False):
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
        if st.button("➕ Add Holding"):

            ticker = ticker_input.upper()

            price_data = get_stock_data(ticker)
            if price_data["price"] is None:
                st.error(
                    "Unable to retrieve stock price. Check the ticker."
                )
                st.stop()

            existing_holding = None

            for holding in st.session_state.portfolio:

                if holding["ticker"] == ticker:

                    existing_holding = holding
                    break

            if existing_holding:

                existing_holding["shares"] += shares_input
                existing_holding["price"] = price_data["price"]
                existing_holding["sector"] = price_data["sector"]
                
            else:
            
                st.session_state.portfolio.append(
                    {
                        "ticker": ticker,
                        "shares": shares_input,
                        "price": price_data["price"],
                        "sector": price_data["sector"]
                    }
                )
                st.write(st.session_state.portfolio)
            st.rerun()
        
        if st.session_state.portfolio:

            holdings_list = [
                holding["ticker"]
                for holding in st.session_state.portfolio
            ]

            selected_stock = st.selectbox(
                "Select a stock to remove",
                holdings_list
            )
            if st.button("➖ Remove Holding"):

                st.session_state.portfolio = [
                    holding
                    for holding in st.session_state.portfolio
                    if holding["ticker"] != selected_stock
                ]

                st.success(
                    f"{selected_stock} removed from portfolio"
                )
                st.rerun()
        if st.button("🔄 Refresh Portfolio Prices"):

            with st.spinner("Refreshing portfolio prices..."):
                    
                refresh_portfolio_prices(
                    st.session_state.portfolio
                )
            st.success("Portfolio prices updated")
            st.rerun()