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
    snp500_tickers
)

st.set_page_config(
    page_title="Correlation Heatmap",
    page_icon="📈"
)

st.header("Correlation Heatmap")
st.write("Visualize the correlation between different stocks in your portfolio.")
tickers = st.multiselect("Select Stocks for Correlation Heatmap", snp500_tickers, default=["AAPL", "MSFT", "GOOGL"])
period = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"])


if st.button("Generate Correlation Heatmap"):
    tickers_list = list(tickers)
    stock_data = get_portfolio_history(tickers_list, period=period)
    fig = plot_correlation_heatmap(stock_data)
    st.plotly_chart(fig, use_container_width=True)

st.title("What is a Correlation Heatmap?")
st.write("""
A correlation heatmap is a graphical representation of the correlation matrix between multiple variables, in this case, stock prices. It uses color gradients to indicate the strength and direction of correlations, making it easy to identify relationships between different stocks. Positive correlations are typically shown in warmer colors (e.g., red), while negative correlations are shown in cooler colors (e.g., blue). This tool is useful for investors to understand how different assets in their portfolio may move in relation to each other, aiding in diversification and risk management strategies.
""")