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
    efficient_frontier_analysis_with_monte_carlo
)

st.set_page_config(
    page_title="Monte Carlo Geometric Brownian Motion Simulation",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.header("Monte Carlo Geometric Brownian Motion Simulation")
st.write("Simulate future stock prices using Geometric Brownian Motion.")
tickers = st.text_input("Enter stock tickers (comma-separated)", "AAPL, MSFT, GOOGL")
weights_input = st.text_input("Enter corresponding weights (comma-separated)", "0.33, 0.33, 0.34")
period = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
start_value = st.number_input("Starting Portfolio Value ($)", min_value=1000, max_value=10000000, value=100000)
num_simulations = st.number_input("Number of Simulations", min_value=100, max_value=5000, value=500)
time_horizon = st.number_input("Time Horizon (days)", min_value=1, max_value=252, value=252)

if st.button("Run Simulation"):
        tickers_list = [t.strip() for t in tickers.split(",")]
        weights = [float(w.strip()) for w in weights_input.split(",")]
        portfolio_data = get_portfolio_history(tickers_list, period=period)
        
        with st.spinner('Running Monte Carlo simulation...'):
            paths = geometric_brownian_motion(portfolio_data, weights, start_value, time_horizon, num_simulations)
        
        st.success('Simulation complete!')
        final_values = paths[:, -1]
        st.subheader("Simulation Results")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("5th Percentile (Worst Case)", f"${np.percentile(final_values, 5):,.0f}")
        with col2:
            st.metric("Expected Value (Mean)", f"${final_values.mean():,.0f}")
        with col3:
            st.metric("95th Percentile (Best Case)", f"${np.percentile(final_values, 95):,.0f}")


        plt.figure(figsize=(12, 6))
        plt.plot(paths.T, color='blue', alpha=0.05, linewidth=0.5)
        plt.plot(paths.mean(axis=0), color='firebrick', linewidth=2.5, label='Average Path(Mean)')
        percentile_05 = np.percentile(paths, 5, axis=0)
        percentile_95 = np.percentile(paths, 95, axis=0)
        plt.plot(percentile_95, color='green', linestyle='--', linewidth=1.5, label='%95 Optimistic Scenario')
        plt.plot(percentile_05, color='orange', linestyle='--', linewidth=1.5, label='%5 Pessimistic Scenario')
        plt.axhline(y=100000, color='black', linestyle=':', label='Starting Value (100k)')
        plt.title(f"Portfolio Future Simulation ({period} / {num_simulations} Simulations)", fontsize=14)
        plt.xlabel("Future Business Days")
        plt.ylabel("Portfolio Value ($)")
        plt.legend(loc='upper left')
        plt.grid(True, alpha=0.3)

        st.pyplot(plt)

st.write("Use run simulation to generate possible future portfolio values based on historical data and the GBM model.")

st.title("What is Geometric Brownian Motion?")
st.write("""
Geometric Brownian Motion (GBM) is a mathematical model used to simulate the random behavior of asset prices over time. It assumes that the logarithm of asset prices follows a Brownian motion with drift, meaning that prices can move up or down in a continuous manner influenced by both predictable trends (drift) and random fluctuations (volatility). GBM is widely used in financial modeling, particularly for option pricing and risk management, as it captures the essential characteristics of financial markets, such as the tendency for prices to grow exponentially over time while also exhibiting randomness.
""")

left, mid, right = st.columns([1, 2, 1])
with mid:
    st.image(
        "https://wikimedia.org/api/rest_v1/media/math/render/svg/f2a3c0d1dcb510719effde045c26f1a9d0b9cb2d",
        caption="Stochastical differential equation Formula",
        width=400,
    )
    st.latex(r"S(t) = S(0) \cdot e^{(\mu - \frac{1}{2} \sigma^2)t + \sigma W(t)}")
    st.write("**Analytical formula of Geometric Brownian Motion:**")
    st.write("- S(t): Asset price at time t")
    st.write("- S(0): Initial asset price")
    st.write("- μ: Drift coefficient (expected return)")
    st.write("- σ: Volatility coefficient (standard deviation of returns)")
    st.write("- W(t): Standard Brownian motion (Wiener process) at time t")
    st.write("- t: Time horizon")


st.write("""**Note:** This simulation provides a statistical view of potential future portfolio values based on historical data and the GBM model. It does not predict actual future prices and should be used for educational and risk assessment purposes only.""")