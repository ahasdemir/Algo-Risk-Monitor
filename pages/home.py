import streamlit as st


st.set_page_config(
    page_title="The Algo Risk Monitor",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Algo Risk Monitor")
st.write("In financial markets, price trends often mask the underlying risk. **Algo-Risk Monitor** is a quantitative analysis tool that now blends **technical momentum signals** with **multi-layered risk analytics** (parametric & historical VaR, portfolio stress tests, Monte Carlo) to turn raw market data into actionable insight. It leverages **Logarithmic Returns** for statistical accuracy, calculates **Annualized Volatility** to standardize risk across timeframes, and layers on **RSI/SMA momentum**, **efficient frontier search**, and **scenario simulations**.")

st.write("- Use the navigation menu on the left to explore different features of the Algo Risk Monitor.", )
st.write("- Each page offers interactive inputs to customize analyses based on your portfolio and risk preferences.")
st.write("- Visualizations and metrics are dynamically generated to provide clear insights into portfolio performance and risk.")
st.write("**Get started by selecting a page from the menu!**")


st.write("**Legal Disclaimer:** This tool is for educational purposes only and should not be considered financial advice. Always consult with a qualified financial advisor before making investment decisions.")