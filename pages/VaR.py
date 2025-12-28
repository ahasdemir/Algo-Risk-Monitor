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
    efficient_frontier_analysis_with_monte_carlo
)

st.header("Value at Risk (VaR) Analysis")
st.write("Calculate the Value at Risk for your portfolio using different methods.")
tickers = st.text_input("Enter stock tickers (comma-separated)", "AAPL, MSFT, GOOGL")
weights_input = st.text_input("Enter corresponding weights (comma-separated)", "0.33, 0.33, 0.34")
period = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"], index=3)
portfolio_value = st.number_input("Portfolio Value ($)", min_value=1000, max_value=10000000, value=100000)
confidence_level = st.slider("Confidence Level (%)", min_value=90, max_value=99, value=95) / 100
    
if st.button("Calculate VaR"):
    tickers_list = [t.strip() for t in tickers.split(",")]
    weights = [float(w.strip()) for w in weights_input.split(",")]
    portfolio_data = get_portfolio_history(tickers_list, period=period)
        
    parametric_var, port_vol = parametric_var_portfolio(portfolio_data, weights, portfolio_value, confidence_level)
    historical_var = historical_var_portfolio(portfolio_data, weights, portfolio_value, confidence_level)
        
    st.subheader("Value at Risk Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Parametric VaR", f"${parametric_var:,.2f}")
    with col2:
        st.metric("Historical VaR", f"${historical_var:,.2f}")
    with col3:
        st.metric("Portfolio Volatility", f"{port_vol:.2%}")

st.title("What is Value at Risk (VaR)?")
st.write("""
Value at Risk (VaR) is a statistical measure used to assess the level of financial risk within a portfolio or investment over a specific time frame. It estimates the maximum potential loss that could occur with a given confidence level. For example, a 95% one-day VaR of $1,000 means that there is a 95% chance that the portfolio will not lose more than $1,000 in a single day.
""")