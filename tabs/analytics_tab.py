import streamlit as st
import pandas as pd

from src.portfolio.portfolio_performance import calculate_portfolio_history
from src.portfolio.performance_metrics import calculate_total_return, calculate_volatility, calculate_sharpe_ratio
from src.portfolio.benchmark import get_benchmark_history, normalize_series, calculate_benchmark_return
from src.portfolio.risk_metrics import calculate_max_drawdown, calculate_best_day, calculate_worst_day
from src.visualizations.risk_charts import create_drawdown_chart, create_returns_distribution


def show_analytics_tab():

    st.header("📊 Portfolio Analytics")

    if "portfolio" not in st.session_state or not st.session_state.portfolio:
        st.warning("Add holdings to view analytics.")
        return

    st.subheader("📈 Portfolio Growth Over Time")


    if st.session_state.portfolio:

        portfolio_history = calculate_portfolio_history(
            st.session_state.portfolio
        )
        st.line_chart(portfolio_history)
        st.subheader("Performance Metrics")


        total_return = calculate_total_return(
            portfolio_history
        )

        volatility = calculate_volatility(
            portfolio_history
        )

        sharpe_ratio = calculate_sharpe_ratio(
            portfolio_history
        )
        
        max_drawdown = calculate_max_drawdown(
            portfolio_history
        )

        best_day = calculate_best_day(
            portfolio_history
        )

        worst_day = calculate_worst_day(
            portfolio_history
        )


        col1, col2, col3 = st.columns(3)


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


        with col3:

            st.metric(
                "Sharpe Ratio",
                f"{sharpe_ratio:.2f}"
            )

        st.subheader("📉 Portfolio Drawdown Risk")
            

        col1, col2, col3 = st.columns(3)


        with col1:
            st.metric(
                "Maximum Drawdown",
                f"{max_drawdown:.2%}"
            )


        with col2:
            st.metric(
                "Best Day",
                f"{best_day:.2%}"
            )


        with col3:
            st.metric(
                "Worst Day",
                f"{worst_day:.2%}"
            )
    
        st.subheader("Risk Visualization")
        drawdown_fig = create_drawdown_chart(
            portfolio_history
        )


        st.plotly_chart(
            drawdown_fig,
            use_container_width=True
        )


        returns_fig = create_returns_distribution(
            portfolio_history
        )


        st.plotly_chart(
            returns_fig,
            use_container_width=True
        )

        st.subheader("📊 Portfolio Performance vs Market Benchmark")


        benchmark_history = get_benchmark_history()


        comparison_df = pd.DataFrame(
            {
                "Portfolio": normalize_series(portfolio_history),
                "S&P 500": normalize_series(benchmark_history)
            }
        )


        comparison_df = comparison_df.dropna()


        st.line_chart(
            comparison_df
        )
        st.subheader("Benchmark Performance")


        portfolio_return = calculate_total_return(
            portfolio_history
        )


        benchmark_return = calculate_benchmark_return(
            benchmark_history
        )


        alpha = (
            portfolio_return
            -
            benchmark_return
        )


        col1, col2, col3 = st.columns(3)


        with col1:
            st.metric(
                "Portfolio Return",
                f"{portfolio_return:.2%}"
            )


        with col2:
            st.metric(
                "S&P 500 Return",
                f"{benchmark_return:.2%}"
            )


        with col3:
            st.metric(
                "Alpha",
                f"{alpha:.2%}"
            )
        
        