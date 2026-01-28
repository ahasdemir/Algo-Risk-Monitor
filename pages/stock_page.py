import streamlit as st
import pandas as pd
import numpy as np
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
    popular_crypto_tickers,
)

st.set_page_config(
    page_title="Stock Price Analysis",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.header("Stock Price Analysis")
st.write("Analyze historical stock prices and visualize key indicators.")

ticker = st.selectbox(
    "Select Stock Ticker", snp500_tickers + popular_crypto_tickers, index=snp500_tickers.index("AAPL")
)
period = st.selectbox(
    "Select Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"], index=5
)

if st.button("Get Stock Data"):
    df = get_stock_data(ticker, period)
    if df is None or df.empty:
        st.error(
            "Failed to retrieve data. Please check the ticker symbol and try again."
        )
    else:
        st.subheader(f"Historical Data for {ticker}")
        st.dataframe(df.tail())

        df_indicators = add_indicators(df)

        fig = go.Figure()
        fig.add_trace(
            go.Candlestick(
                x=df_indicators.index,
                open=df_indicators["Open"],
                high=df_indicators["High"],
                low=df_indicators["Low"],
                close=df_indicators["Close"],
                name="OHLC",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df_indicators.index,
                y=df_indicators["SMA_20"],
                mode="lines",
                name="20-day SMA",
                line=dict(color="orange"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df_indicators.index,
                y=df_indicators["SMA_50"],
                mode="lines",
                name="50-day SMA",
                line=dict(color="blue"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df_indicators.index,
                y=df_indicators["SMA_200"],
                mode="lines",
                name="200-day SMA",
                line=dict(color="red"),
            )
        )

        fig.update_layout(
            title=f"{ticker} Chart with Moving Averages",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            xaxis_rangeslider_visible=False,
        )
        st.plotly_chart(fig)

        st.subheader("Volatility Analysis")
        vol_fig = volatility_analysis(df)
        st.plotly_chart(vol_fig)
