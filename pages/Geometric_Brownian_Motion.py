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

    # Graph of simulation paths
        st.subheader("Monte Carlo Simulation Paths")
        fig = go.Figure()
        for i in range(min(num_simulations, 100)):  # Plot only first
            fig.add_trace(go.Scatter(y=paths[i], mode='lines', line=dict(width=1), name=f'Simulation {i+1}', opacity=0.3))

        fig.update_layout(title='Monte Carlo Simulation of Portfolio Value',
                          xaxis_title='Days',
                          yaxis_title='Portfolio Value ($)')
        
        fig.add_hline(y=start_value, line_dash="dash", line_color="green",
                        annotation_text="Starting Value", annotation_position="top left")
        
        fig.add_hline(y=final_values.mean(), line_dash="dash", line_color="blue",
                        annotation_text="Expected Value", annotation_position="top left")
        
        fig.add_trace(y=np.percentile(final_values, 5), line_dash="dash", line_color="red",
                        annotation_text="5th Percentile", annotation_position="top left")
        
        fig.add_trace(y=np.percentile(final_values, 95), line_dash="dash", line_color="orange",
                        annotation_text="95th Percentile", annotation_position="top left")
        
        st.plotly_chart(fig, use_container_width=True)
