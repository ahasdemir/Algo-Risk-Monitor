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



home = st.Page("pages/home.py", title="Home", icon=":material/dashboard:")
gbm = st.Page("pages/Geometric_Brownian_Motion.py", title="Geomatric Brownian Motion Simulation")
portfolio_performance = st.Page("pages/portfolio_performance.py", title="Portfolio Performance")

pg = st.navigation([home, gbm, portfolio_performance])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()
