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
    snp500_tickers
)

st.set_page_config(
    page_title="Monte Carlo Geometric Brownian Motion Simulation",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.header("Monte Carlo Geometric Brownian Motion Simulation")
st.write("Simulate future stock prices using Geometric Brownian Motion.")
tickers = st.multiselect("Select Stocks for GBM Simulation", snp500_tickers, default=["AAPL", "MSFT", "GOOGL"])
weights_input = st.text_input("Enter corresponding weights (comma-separated)", "0.33, 0.33, 0.34")
period = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
start_value = st.number_input("Starting Portfolio Value ($)", min_value=1000, max_value=10000000, value=100000)
num_simulations = st.number_input("Number of Simulations", min_value=100, max_value=5000, value=500)
time_horizon = st.number_input("Time Horizon (days)", min_value=1, max_value=252, value=252)

if st.button("Run Simulation"):
        tickers_list = list(tickers)
        try:
            weights = [float(w.strip()) for w in weights_input.split(",")]
        except ValueError:
            st.error("Weights must be numeric values separated by commas.")
            st.stop()

        if len(weights) != len(tickers_list):
            st.error("Number of tickers and weights do not match. Please check.")
            st.stop()

        # Normalize weights if they don't sum to 1 to avoid user input issues
        weight_sum = sum(weights)
        if weight_sum == 0:
            st.error("Sum of weights cannot be zero.")
            st.stop()
        weights = [w / weight_sum for w in weights]

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


        fig = go.Figure()

        # 1. Spagetti Çizgileri (Performans için sadece ilk 50 tanesini çizelim)
        # Hepsini çizersen tarayıcı donabilir.
        for i in range(min(50, paths.shape[0])):
            fig.add_trace(go.Scatter(
                y=paths[i, :],
                mode='lines',
                line=dict(color='rgba(50, 0, 220, 0.1)', width=1),
                showlegend=False
            ))

        # 2. Ortalama ve Güven Aralıkları
        mean_path = paths.mean(axis=0)
        worst_case = np.percentile(paths, 5, axis=0)
        best_case = np.percentile(paths, 95, axis=0)

        fig.add_trace(go.Scatter(y=mean_path, mode='lines', name='Expected Value (Mean)', line=dict(color='red', width=3)))
        fig.add_trace(go.Scatter(y=best_case, mode='lines', name='95th Percentile (Best Case)', line=dict(color='green', dash='dash')))
        fig.add_trace(go.Scatter(y=worst_case, mode='lines', name='5th Percentile (Worst Case)', line=dict(color='orange', dash='dash')))

        fig.update_layout(
            title=f"GBM Simulation ({num_simulations} Scenarios)",
            xaxis_title="Trading Day",
            yaxis_title="Portfolio Value ($)",
            hovermode="x"
        )

        st.plotly_chart(fig, use_container_width=True)

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