import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns
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
    page_title="Value at Risk (VaR) Analysis",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.header("Value at Risk (VaR) Analysis")
st.write("Calculate the Value at Risk for your portfolio using different methods.")
tickers = st.multiselect(
    "Select Stocks for VaR Analysis", snp500_tickers, default=["AAPL", "MSFT", "GOOGL"]
)
weights_input = st.text_input(
    "Enter corresponding weights (comma-separated)", "0.33, 0.33, 0.34"
)
use_equal_weights = st.checkbox("Use equal weights", value=False)
period = st.selectbox(
    "Select Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"], index=3
)
portfolio_value = st.number_input(
    "Portfolio Value ($)", min_value=1000, max_value=10000000, value=100000
)
confidence_level = (
    st.slider("Confidence Level (%)", min_value=90, max_value=99, value=95) / 100
)

if st.button("Calculate VaR"):
    tickers_list = list(tickers)
    if len(tickers_list) == 0:
        st.error("Please select at least one ticker.")
        st.stop()

    if use_equal_weights:
        weights = [1 / len(tickers_list)] * len(tickers_list)
    else:
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

    parametric_var, port_vol = parametric_var_portfolio(
        portfolio_data, weights, portfolio_value, confidence_level
    )
    historical_var = historical_var_portfolio(
        portfolio_data, weights, portfolio_value, confidence_level
    )

    st.subheader("Value at Risk Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Parametric VaR", f"${parametric_var:,.2f}")
    with col2:
        st.metric("Historical VaR", f"${historical_var:,.2f}")
    with col3:
        st.metric("Portfolio Volatility", f"{port_vol:.2%}")

    portfolio_hist_ret = portfolio_data.dot(np.array(weights)).dropna()

    # 2. %1'lik Sınırı Bul (Percentile)
    cutoff = np.percentile(portfolio_hist_ret, (1 - confidence_level) * 100)

    # --- GRAFİK ---
    plt.figure(figsize=(12, 6))

    # Histogram (Dağılım)
    sns.histplot(
        portfolio_hist_ret,
        bins=50,
        kde=True,
        color="skyblue",
        label="Daily Returns Distribution",
    )

    # VaR Çizgisi (Kırmızı Çizgi)
    plt.axvline(
        x=cutoff,
        color="red",
        linestyle="--",
        linewidth=3,
        label=f"VaR ({confidence_level:.0%}): {cutoff:.2%}",
    )

    # Süsleme
    plt.title("Historical Return Distribution and Risk Threshold", fontsize=14)
    plt.xlabel("Daily Return")
    plt.ylabel("Frequency (Number of Days)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Sol taraftaki "Kuyruk" (Tail) bölgesini boya
    plt.axvspan(portfolio_hist_ret.min(), cutoff, color="red", alpha=0.2)

    st.pyplot(plt)

st.title("What is Value at Risk (VaR)?")
st.write(
    """
Value at Risk (VaR) is a statistical measure used to assess the level of financial risk within a portfolio or investment over a specific time frame. It estimates the maximum potential loss that could occur with a given confidence level. For example, a 95% one-day VaR of $1,000 means that there is a 95% chance that the portfolio will not lose more than $1,000 in a single day.
"""
)
