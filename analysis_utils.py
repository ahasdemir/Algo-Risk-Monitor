import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

@st.cache_data
def get_stock_data(ticker, period="1y"):
    df = yf.download(ticker, period=period, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    df["Log_Return"] = np.log(df["Close"] / df["Close"].shift(1))
    return df

def add_indicators(df):
    df["SMA_20"] = df["Close"].rolling(20).mean()
    df["SMA_50"] = df["Close"].rolling(50).mean()
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    return df

def volatility_analysis(df):
    df["Volatility"] = df["Log_Return"].rolling(21).std() * np.sqrt(252)
    return df

@st.cache_data
def get_portfolio_history(symbols, period='1y'):
    portfolio_df = pd.DataFrame()
    
    for symbol in symbols:
        data = get_stock_data(symbol, period=period) 
        portfolio_df[symbol] = data['Log_Return']
        
    return portfolio_df

def portfolio_performance_with_data(portfolio_df, weights, period='1y'):
    expected_returns = portfolio_df.mean() * 252
    covariance_matrix = portfolio_df.cov() * 252
    weights = np.array(weights)
    portfolio_return = np.sum(expected_returns * weights)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
    return portfolio_return, portfolio_volatility


def calculate_parametric_var(df, portfolio_value=100000, confidence_level=0.95, day=1):
    """
    Hull'un 'Linear Model'ini (Parametrik VaR) kullanarak riski hesaplar.
    """
    
    current_annual_volatility = df['Volatility'].iloc[-1]
    
    daily_volatility = current_annual_volatility / np.sqrt(252)

    z_score = norm.ppf(confidence_level)

    var_value = portfolio_value * daily_volatility * z_score * np.sqrt(day)
    
    return var_value, current_annual_volatility


def calculate_historical_var(df, portfolio_value=100000, confidence_level=0.95, day=1):
    """
    Tarihsel Simülasyon yöntemi ile VaR hesaplar.
    """

    # 1. Eğer vade 1 günden fazlaysa, geçmişteki o vadeli getirileri oluştur
    if day == 1:
        # 1 günse olduğu gibi al
        period_returns = df['Log_Return'].dropna()
    else:
        period_returns = df['Log_Return'].rolling(window=day).sum().dropna()
    
    # VaR yüzdesini hesapla
    var_percentile = np.percentile(period_returns, (1 - confidence_level) * 100)
    
    var_value = portfolio_value * abs(var_percentile)
    
    return var_value

def parametric_var_portfolio(df_portfolio, weights, portfolio_value=100000, confidence_level=0.95, day=1):
    """
    Portföy için Hull'un 'Linear Model'ini (Parametrik VaR) kullanarak riski hesaplar.
    """
    weights = np.array(weights)
    
    portfolio_volatility = portfolio_performance_with_data(df_portfolio, weights)[1]
    
    daily_volatility = portfolio_volatility / np.sqrt(252)

    z_score = norm.ppf(confidence_level)

    var_value = portfolio_value * daily_volatility * z_score * np.sqrt(day)
    
    return var_value, portfolio_volatility


def historical_var_portfolio(df_portfolio, weights, portfolio_value=100000, confidence_level=0.95, day=1):
    """
    Portföy için 'Historical Simulation' (Gerçek Veri) VaR hesabı.
    Ağırlıklandırılmış geçmiş getirileri kullanır.
    """
    weights = np.array(weights)
    
    portfolio_historical_returns = df_portfolio.dot(weights)
    portfolio_historical_returns = portfolio_historical_returns.dropna()
    # 2. ADIM: Rolling Sum (Doğru Historical Yöntem)
    if day > 1:
        portfolio_historical_returns = portfolio_historical_returns.rolling(window=day).sum().dropna()
    
    # 3. ADIM: Percentile
    var_percentile = np.percentile(portfolio_historical_returns, (1 - confidence_level) * 100)
    
    return portfolio_value * abs(var_percentile)

def geometric_brownian_motion(df_portfolio, weights, start_value=100000, days=252, simulations=500):
    """
    Geometric Brownian Motion kullanarak portföy simülasyonu yapar.
    """
    weights = np.array(weights)
    portfolio_daily_returns = df_portfolio.dot(weights)
    mu_p = portfolio_daily_returns.mean()          # Portföyün Günlük Drift'i
    sigma_p = portfolio_daily_returns.std()        # Portföyün Günlük Volatilitesi

    # Monte Carlo Motoru
    random_shocks = np.random.normal(0, 1, (simulations, days))
    drift_component = (mu_p - 0.5 * sigma_p**2)
    shock_component = sigma_p * random_shocks
    daily_log_returns = drift_component + shock_component

    portfolio_paths = np.zeros((simulations, days + 1))
    portfolio_paths[:, 0] = start_value 
    portfolio_paths[:, 1:] = start_value * np.exp(np.cumsum(daily_log_returns, axis=1))

    return portfolio_paths

def efficient_frontier_analysis_with_monte_carlo(df_portfolio, num_portfolios=10000, period="1y", seed=None):
    if seed is not None:
        np.random.seed(seed)

    tickers = df_portfolio.columns.tolist()
    n = len(tickers)
    all_weights = np.zeros((num_portfolios, n))
    ret_arr = np.zeros(num_portfolios)
    vol_arr = np.zeros(num_portfolios)
    sharpe_arr = np.zeros(num_portfolios)

    print(f"{num_portfolios} senaryo hesaplanıyor... for {period}")

    for i in range(num_portfolios):
        w = np.random.random(n)
        w /= w.sum()
        all_weights[i, :] = w
        ret, vol = portfolio_performance_with_data(df_portfolio, list(w), period=period)
        ret_arr[i] = ret
        vol_arr[i] = vol
        sharpe_arr[i] = ret / vol if vol != 0 else 0

    max_idx = sharpe_arr.argmax()
    return max_idx, ret_arr[max_idx], vol_arr[max_idx], all_weights[max_idx, :]