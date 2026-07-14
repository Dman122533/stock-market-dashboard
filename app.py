import streamlit as st
from tabs.stock_tab import show_stock_tab
from tabs.portfolio_tab import show_portfolio_tab
from tabs.analytics_tab import show_analytics_tab
from database.database import create_tables
from database.auth import login_user, create_user

st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)
create_tables()

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:

    st.title("📈 Stock Market Dashboard")

    login_tab, create_tab = st.tabs(
        [
            "Login",
            "Create Account"
        ]
    )


    with login_tab:

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )


        if st.button("Login"):

            user = login_user(
                username,
                password
            )

            if user:

                st.session_state.user = user

                st.rerun()

            else:

                st.error(
                    "Invalid username or password"
                )


    with create_tab:

        new_username = st.text_input(
            "Create Username"
        )

        new_password = st.text_input(
            "Create Password",
            type="password"
        )


        if st.button("Create Account"):

            if not new_username or not new_password:

                st.warning(
                    "Please enter a username and password."
                )

            else:

                success = create_user(
                    new_username,
                    new_password
                )

                if success:

                    st.success(
                        "Account created! You can now login."
                    )

                else:

                    st.error(
                        "Username already exists."
                    )


    st.stop()

st.title("📈 Stock Market Dashboard")

col1, col2 = st.columns([5,1])

with col1:
    st.write(
        f"👋 Welcome, {st.session_state.user['username']}"
    )

with col2:
    if st.button("🚪 Logout"):

        st.session_state.user = None

        if "portfolio" in st.session_state:
            del st.session_state.portfolio

        st.rerun()
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