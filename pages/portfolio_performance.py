import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
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
    efficient_frontier_analysis_with_monte_carlo,
    plot_correlation_heatmap,
    snp500_tickers
)

st.set_page_config(
    page_title="Portfolio Performance Analysis",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.header("Portfolio Performance Analysis")
st.write("Analyze the performance of your portfolio over time.")

tickers = st.multiselect("Select Stocks for Portfolio Analysis", snp500_tickers, default=["AAPL", "MSFT", "GOOGL"])
weights_input = st.text_input("Enter corresponding weights (comma-separated)", "0.4, 0.4, 0.2")
period = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"])

if st.button("Analyze Portfolio Performance"):
    tickers_list = list(tickers)
    try:
        weights = [float(w.strip()) for w in weights_input.split(",")]
    except ValueError:
        st.error("Weights must be numeric values separated by commas.")
        st.stop()

    if len(weights) != len(tickers_list):
        st.error("Number of tickers and weights do not match. Please check.")
        st.stop()

    weight_sum = sum(weights)
    if weight_sum == 0:
        st.error("Sum of weights cannot be zero.")
        st.stop()
    weights = [w / weight_sum for w in weights]
    portfolio_data = get_portfolio_history(tickers_list, period=period)
    portfolio_return, portfolio_volatility = portfolio_performance_with_data(portfolio_data, weights, period=period)
        
    st.subheader("Portfolio Performance Results")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Expected Annual Return", f"{portfolio_return:.2%}")
    with col2:
        st.metric("Portfolio Volatility (Risk)", f"{portfolio_volatility:.2%}")
        
    st.dataframe(portfolio_data.tail(10), use_container_width=True)

st.title("What is Portfolio Performance?")
st.write("""
Portfolio performance analysis involves evaluating the returns and risks associated with a portfolio of investments. It uses basic financial metrics such as expected return and volatility to help investors understand how their portfolio is likely to perform under various market conditions. This analysis aids in making informed investment decisions and optimizing asset allocation. This is not a forecast or guarantee of future performance; actual results may vary. This analysis just does basic calculations based on historical data. Gives you returns in given period and annualized volatility.
""")