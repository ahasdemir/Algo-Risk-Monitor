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
    page_title="The Algo Risk Monitor",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Menu for navigation
st.sidebar.title("Navigation")
menu_options = ["Home", "Indicator Analysis", "Volatility Analysis",
                "Portfolio Performance", "Value at Risk (VaR)", "Monte Carlo Simulation", "Efficient Frontier"]


menu_options_selection = st.sidebar.radio("Go to", menu_options)
if menu_options_selection == "Home":
    st.title("The Algo Risk Monitor")
    st.write("Welcome to The Algo Risk Monitor! This application helps you monitor and manage the risks associated with your algorithmic trading strategies.")
    st.header("Home")
    st.write("Use the sidebar to navigate through different risk analysis tools.")
    st.write("This application provides various functionalities to help you analyze and manage the risks in your trading strategies.")
elif menu_options_selection == "Portfolio Performance":
    st.header("Portfolio Performance Analysis")
    st.write("Analyze the performance of your portfolio over time.")

    tickers = st.text_input("Enter stock tickers (comma-separated)", "AAPL, MSFT, GOOGL")
    weights_input = st.text_input("Enter corresponding weights (comma-separated)", "0.4, 0.4, 0.2")
    period = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"])

    if st.button("Analyze Portfolio Performance"):
        tickers_list = [t.strip() for t in tickers.split(",")]
        weights = [float(w.strip()) for w in weights_input.split(",")]
        portfolio_data = get_portfolio_history(tickers_list, period=period)
        portfolio_return, portfolio_volatility = portfolio_performance_with_data(portfolio_data, weights, period=period)
        
        st.subheader("Portfolio Performance Results")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Expected Annual Return", f"{portfolio_return:.2%}")
        with col2:
            st.metric("Portfolio Volatility (Risk)", f"{portfolio_volatility:.2%}")
        
        st.dataframe(portfolio_data.tail(10), use_container_width=True)


elif menu_options_selection == "Value at Risk (VaR)":
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
elif menu_options_selection == "Monte Carlo Simulation":
    st.header("Monte Carlo Simulation")
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
            fig.add_trace(go.Scatter(y=paths[i], mode='lines', line=dict(width=1), name=f'Simulation {i+1}'))
        fig.update_layout(title='Monte Carlo Simulation of Portfolio Value',
                          xaxis_title='Days',
                          yaxis_title='Portfolio Value ($)')
        fig.add_hline(y=start_value, line_dash="dash", line_color="green",
                        annotation_text="Starting Value", annotation_position="top left")
        fig.add_hline(y=final_values.mean(), line_dash="dash", line_color="blue",
                        annotation_text="Expected Value", annotation_position="top left")
        fig.add_hline(y=np.percentile(final_values, 5), line_dash="dash", line_color="red",
                        annotation_text="5th Percentile", annotation_position="top left")
        fig.add_hline(y=np.percentile(final_values, 95), line_dash="dash", line_color="orange",
                        annotation_text="95th Percentile", annotation_position="top left")
        st.plotly_chart(fig, use_container_width=True)

elif menu_options_selection == "Efficient Frontier":
    st.header("Efficient Frontier Analysis")
    st.write("Analyze the efficient frontier of your portfolio using Monte Carlo simulations.")
    tickers = st.text_input("Enter stock tickers (comma-separated)", "AAPL, MSFT, GOOGL")
    period = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
    num_portfolios = st.number_input("Number of Portfolios to Simulate", min_value=100, max_value=10000, value=5000)
    
    if st.button("Analyze Efficient Frontier"):
        tickers_list = [t.strip() for t in tickers.split(",")]
        portfolio_data = get_portfolio_history(tickers_list, period=period)
        
        with st.spinner('Running efficient frontier analysis...'):
            max_idx, best_ret, best_vol, best_w = efficient_frontier_analysis_with_monte_carlo(portfolio_data, num_portfolios, period)
        
        st.success('Analysis complete!')
        st.subheader("Optimal Portfolio (Max Sharpe Ratio)")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Expected Return", f"{best_ret:.2%}")
        with col2:
            st.metric("Volatility (Risk)", f"{best_vol:.2%}")
        with col3:
            st.metric("Sharpe Ratio", f"{best_ret/best_vol:.2f}")
        
        st.subheader("Optimal Weights")
        weights_df = pd.DataFrame({
            'Ticker': tickers_list,
            'Weight': [f"{w:.2%}" for w in best_w]
        })
        st.dataframe(weights_df, use_container_width=True)
elif menu_options_selection == "Indicator Analysis":
    st.header("Indicator Analysis")
    st.write("Analyze various technical indicators for a given stock.")
    ticker = st.text_input("Enter stock ticker", "AAPL")
    period = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
    
    if st.button("Analyze Indicators"):
        stock_data = get_stock_data(ticker, period=period)
        indicator_data = add_indicators(stock_data)
        
        st.subheader(f"{ticker} Technical Indicators")
        st.line_chart(indicator_data[['Close', 'SMA_20', 'SMA_50']])
        st.line_chart(indicator_data['RSI'])
        st.dataframe(indicator_data[['Close', 'SMA_20', 'SMA_50', 'RSI']].tail(10), use_container_width=True)
elif menu_options_selection == "Volatility Analysis":
    st.header("Volatility Analysis")
    st.write("Analyze the volatility of a given stock.")
    ticker = st.text_input("Enter stock ticker", "AAPL")
    period = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
    
    if st.button("Analyze Volatility"):
        stock_data = get_stock_data(ticker, period=period)
        stock_data = volatility_analysis(stock_data)
        
        st.subheader(f"{ticker} Volatility Analysis")
        current_vol = stock_data['Volatility'].iloc[-1]
        st.metric("Current Annualized Volatility", f"{current_vol:.2%}")
        
        st.line_chart(stock_data[['Close']])
        st.line_chart(stock_data['Volatility'])
        st.dataframe(stock_data[['Close', 'Log_Return', 'Volatility']].tail(10), use_container_width=True)
