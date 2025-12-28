import streamlit as st
from analysis_utils import (
    get_stock_data,
    add_indicators,
    volatility_analysis,
    get_portfolio_history,
    portfolio_performance_with_data,
    calculate_parametric_var,
    calculate_historical_var,
    parametric_var_portfolio,
    historical_var_portfolio,
    geometric_brownian_motion,
    efficient_frontier_analysis_with_monte_carlo
)

st.set_page_config(
    page_title="The Algo Risk Monitor",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Menu for navigation
st.sidebar.title("Navigation")
menu_options = ["Home", "Indicator Analysis", "Volatility Analysis",
                "Portfolio Performance", "Value at Risk (VaR)", "Monte Carlo Simulation", "Efficient Frontier"]


st.title("The Algo Risk Monitor")
st.write("Welcome to The Algo Risk Monitor! This application helps you monitor and manage the risks associated with your algorithmic trading strategies.")

