import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
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
    snp500_tickers,
)

st.set_page_config(
    page_title="Portfolio Optimization using Efficient Frontier", page_icon="📈"
)

st.header("Portfolio Optimization using Efficient Frontier")
st.write(
    "Optimize your portfolio using the Efficient Frontier method with Monte Carlo simulations."
)
tickers = st.multiselect(
    "Select Stocks for Portfolio Optimization",
    snp500_tickers,
    default=["AAPL", "MSFT", "GOOGL"],
)
num_portfolios = st.number_input(
    "Number of Portfolios to Simulate", min_value=100, max_value=10000, value=1000
)
risk_free_rate = (
    st.number_input("Risk-Free Rate (%)", min_value=0.0, max_value=10.0, value=2.0)
    / 100
)
period = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

if st.button("Optimize Portfolio"):
    tickers_list = list(tickers)
    if len(tickers_list) == 0:
        st.error("Please select at least one ticker.")
        st.stop()

    stock_data = get_portfolio_history(tickers_list, period=period)
    fig, max_sharpe_portfolio, min_vol_portfolio = (
        efficient_frontier_analysis_with_monte_carlo(
            stock_data, num_portfolios=num_portfolios, risk_free_rate=risk_free_rate
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Optimal Portfolios")
    st.write("Portfolio with Maximum Sharpe Ratio:")
    st.write(max_sharpe_portfolio)

    st.write("Portfolio with Minimum Volatility:")
    st.write(min_vol_portfolio)

st.title("What is Efficient Frontier?")
st.write(
    """
The Efficient Frontier is a concept in modern portfolio theory that represents the set of optimal portfolios offering the highest expected return for a defined level of risk or the lowest risk for a given level of expected return. It is a graphical representation of various portfolios that optimally balance risk and return.
"""
)
