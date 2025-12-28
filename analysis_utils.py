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

def efficient_frontier_analysis_with_monte_carlo(df_portfolio, num_portfolios=10000, period="1y", seed=None, risk_free_rate: float = 0.0):
    if seed is not None:
        np.random.seed(seed)

    tickers = df_portfolio.columns.tolist()
    n = len(tickers)
    all_weights = np.zeros((num_portfolios, n))
    ret_arr = np.zeros(num_portfolios)
    vol_arr = np.zeros(num_portfolios)
    sharpe_arr = np.zeros(num_portfolios)

    for i in range(num_portfolios):
        w = np.random.random(n)
        w /= w.sum()
        all_weights[i, :] = w
        ret, vol = portfolio_performance_with_data(df_portfolio, list(w), period=period)
        ret_arr[i] = ret
        vol_arr[i] = vol
        sharpe_arr[i] = (ret - risk_free_rate) / vol if vol != 0 else 0

    # Optimal portfolios
    max_sharpe_idx = sharpe_arr.argmax()
    min_vol_idx = vol_arr.argmin()

    max_sharpe = {
        "tickers": tickers,
        "weights": {tickers[j]: float(all_weights[max_sharpe_idx, j]) for j in range(n)},
        "return": float(ret_arr[max_sharpe_idx]),
        "volatility": float(vol_arr[max_sharpe_idx]),
        "sharpe": float(sharpe_arr[max_sharpe_idx]),
        "risk_free_rate": float(risk_free_rate),
    }

    min_vol = {
        "tickers": tickers,
        "weights": {tickers[j]: float(all_weights[min_vol_idx, j]) for j in range(n)},
        "return": float(ret_arr[min_vol_idx]),
        "volatility": float(vol_arr[min_vol_idx]),
        "sharpe": float(sharpe_arr[min_vol_idx]),
        "risk_free_rate": float(risk_free_rate),
    }

    # Plotly figure for Efficient Frontier
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=vol_arr, y=ret_arr,
        mode="markers",
        name="Simulated Portfolios",
        marker=dict(
            color=sharpe_arr,
            colorscale="Viridis",
            showscale=True,
            size=6,
            opacity=0.7,
            colorbar=dict(title="Sharpe")
        ),
    ))

    fig.add_trace(go.Scatter(
        x=[vol_arr[max_sharpe_idx]], y=[ret_arr[max_sharpe_idx]],
        mode="markers+text",
        name="Max Sharpe",
        marker=dict(color="red", size=10, symbol="star"),
        text=["Max Sharpe"], textposition="top center",
    ))

    fig.add_trace(go.Scatter(
        x=[vol_arr[min_vol_idx]], y=[ret_arr[min_vol_idx]],
        mode="markers+text",
        name="Min Volatility",
        marker=dict(color="orange", size=10, symbol="diamond"),
        text=["Min Vol"], textposition="bottom center",
    ))

    fig.update_layout(
        title=f"Efficient Frontier ({num_portfolios} simulations, period={period}, rf={risk_free_rate:.2%})",
        xaxis_title="Volatility (Std Dev)",
        yaxis_title="Expected Return",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=600,
    )

    return fig, max_sharpe, min_vol

def plot_correlation_heatmap(df):
    corr = df.corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='Portland',
        zmin=-1, zmax=1
    ))
    fig.update_layout(title="Stock Correlation Matrix", height=500)
    return fig

# Full S&P 500 tickers (source: DataHub constituents list, '.' replaced with '-')
snp500_tickers = [
    "MMM", "AOS", "ABT", "ABBV", "ACN", "ADBE", "AMD", "AES", "AFL", "A",
    "APD", "ABNB", "AKAM", "ALB", "ARE", "ALGN", "ALLE", "LNT", "ALL", "GOOGL",
    "GOOG", "MO", "AMZN", "AMCR", "AEE", "AEP", "AXP", "AIG", "AMT", "AWK",
    "AMP", "AME", "AMGN", "APH", "ADI", "AON", "APA", "APO", "AAPL", "AMAT",
    "APTV", "ACGL", "ADM", "ANET", "AJG", "AIZ", "T", "ATO", "ADSK", "ADP",
    "AZO", "AVB", "AVY", "AXON", "BKR", "BALL", "BAC", "BAX", "BDX", "BRK-B",
    "BBY", "TECH", "BIIB", "BLK", "BX", "XYZ", "BK", "BA", "BKNG", "BSX",
    "BMY", "AVGO", "BR", "BRO", "BF-B", "BLDR", "BG", "BXP", "CHRW", "CDNS",
    "CZR", "CPT", "CPB", "COF", "CAH", "KMX", "CCL", "CARR", "CAT", "CBOE",
    "CBRE", "CDW", "COR", "CNC", "CNP", "CF", "CRL", "SCHW", "CHTR", "CVX",
    "CMG", "CB", "CHD", "CI", "CINF", "CTAS", "CSCO", "C", "CFG", "CLX",
    "CME", "CMS", "KO", "CTSH", "COIN", "CL", "CMCSA", "CAG", "COP", "ED",
    "STZ", "CEG", "COO", "CPRT", "GLW", "CPAY", "CTVA", "CSGP", "COST", "CTRA",
    "CRWD", "CCI", "CSX", "CMI", "CVS", "DHR", "DRI", "DDOG", "DVA", "DAY",
    "DECK", "DE", "DELL", "DAL", "DVN", "DXCM", "FANG", "DLR", "DG", "DLTR",
    "D", "DPZ", "DASH", "DOV", "DOW", "DHI", "DTE", "DUK", "DD", "EMN",
    "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "ELV", "EMR", "ENPH", "ETR",
    "EOG", "EPAM", "EQT", "EFX", "EQIX", "EQR", "ERIE", "ESS", "EL", "EG",
    "EVRG", "ES", "EXC", "EXE", "EXPE", "EXPD", "EXR", "XOM", "FFIV", "FDS",
    "FICO", "FAST", "FRT", "FDX", "FIS", "FITB", "FSLR", "FE", "FI", "F",
    "FTNT", "FTV", "FOXA", "FOX", "BEN", "FCX", "GRMN", "IT", "GE", "GEHC",
    "GEV", "GEN", "GNRC", "GD", "GIS", "GM", "GPC", "GILD", "GPN", "GL",
    "GDDY", "GS", "HAL", "HIG", "HAS", "HCA", "DOC", "HSIC", "HSY", "HPE",
    "HLT", "HOLX", "HD", "HON", "HRL", "HST", "HWM", "HPQ", "HUBB", "HUM",
    "HBAN", "HII", "IBM", "IEX", "IDXX", "ITW", "INCY", "IR", "PODD", "INTC",
    "ICE", "IFF", "IP", "IPG", "INTU", "ISRG", "IVZ", "INVH", "IQV", "IRM",
    "JBHT", "JBL", "JKHY", "J", "JNJ", "JCI", "JPM", "K", "KVUE", "KDP",
    "KEY", "KEYS", "KMB", "KIM", "KMI", "KKR", "KLAC", "KHC", "KR", "LHX",
    "LH", "LRCX", "LW", "LVS", "LDOS", "LEN", "LII", "LLY", "LIN", "LYV",
    "LKQ", "LMT", "L", "LOW", "LULU", "LYB", "MTB", "MPC", "MKTX", "MAR",
    "MMC", "MLM", "MAS", "MA", "MTCH", "MKC", "MCD", "MCK", "MDT", "MRK",
    "META", "MET", "MTD", "MGM", "MCHP", "MU", "MSFT", "MAA", "MRNA", "MHK",
    "MOH", "TAP", "MDLZ", "MPWR", "MNST", "MCO", "MS", "MOS", "MSI", "MSCI",
    "NDAQ", "NTAP", "NFLX", "NEM", "NWSA", "NWS", "NEE", "NKE", "NI", "NDSN",
    "NSC", "NTRS", "NOC", "NCLH", "NRG", "NUE", "NVDA", "NVR", "NXPI", "ORLY",
    "OXY", "ODFL", "OMC", "ON", "OKE", "ORCL", "OTIS", "PCAR", "PKG", "PLTR",
    "PANW", "PSKY", "PH", "PAYX", "PAYC", "PYPL", "PNR", "PEP", "PFE", "PCG",
    "PM", "PSX", "PNW", "PNC", "POOL", "PPG", "PPL", "PFG", "PG", "PGR",
    "PLD", "PRU", "PEG", "PTC", "PSA", "PHM", "PWR", "QCOM", "DGX", "RL",
    "RJF", "RTX", "O", "REG", "REGN", "RF", "RSG", "RMD", "RVTY", "ROK",
    "ROL", "ROP", "ROST", "RCL", "SPGI", "CRM", "SBAC", "SLB", "STX", "SRE",
    "NOW", "SHW", "SPG", "SWKS", "SJM", "SW", "SNA", "SOLV", "SO", "LUV",
    "SWK", "SBUX", "STT", "STLD", "STE", "SYK", "SMCI", "SYF", "SNPS", "SYY",
    "TMUS", "TROW", "TTWO", "TPR", "TRGP", "TGT", "TEL", "TDY", "TER", "TSLA",
    "TXN", "TPL", "TXT", "TMO", "TJX", "TKO", "TTD", "TSCO", "TT", "TDG",
    "TRV", "TRMB", "TFC", "TYL", "TSN", "USB", "UBER", "UDR", "ULTA", "UNP",
    "UAL", "UPS", "URI", "UNH", "UHS", "VLO", "VTR", "VLTO", "VRSN", "VRSK",
    "VZ", "VRTX", "VTRS", "VICI", "V", "VST", "VMC", "WRB", "GWW", "WAB",
    "WBA", "WMT", "DIS", "WBD", "WM", "WAT", "WEC", "WFC", "WELL", "WST",
    "WDC", "WY", "WSM", "WMB", "WTW", "WDAY", "WYNN", "XEL", "XYL", "YUM",
    "ZBRA", "ZBH", "ZTS",
]