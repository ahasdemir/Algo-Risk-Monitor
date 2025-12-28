# Algo-Risk Monitor 📈

> **An automated dashboard for *monitoring* market volatility and financial risk metrics.**

  

## 📋 Executive Summary

In financial markets, price trends often mask the underlying risk. **Algo-Risk Monitor** is a quantitative analysis tool that now blends **technical momentum signals** with **multi-layered risk analytics** (parametric & historical VaR, portfolio stress tests, Monte Carlo) to turn raw market data into actionable insight.

It leverages **Logarithmic Returns** for statistical accuracy, calculates **Annualized Volatility** to standardize risk across timeframes, and layers on **RSI/SMA momentum**, **efficient frontier search**, and **scenario simulations**. The notebook produces ready-to-use visual dashboards plus exportable CSV outputs for downstream tooling.

-----

## 🚀 Key Features

  * **Automated Data Pipeline:** Pulls auto-adjusted OHLCV via `yfinance` and normalizes MultiIndex outputs. Supports all 503 S&P 500 constituents.
  * **Momentum + Trend:** RSI, SMA-20/50 crossovers, and price dashboard candlesticks in Plotly.
  * **Volatility + VaR Suite:** 21-day annualized volatility, Hull-style parametric VaR, and historical VaR for both single tickers and weighted portfolios.
  * **Portfolio Analytics:** Expected returns, covariance matrix, efficient frontier exploration (with risk-free rate support), and Monte Carlo search for maximum Sharpe.
  * **Smart Weight Input:** Equal-weight option for quick portfolio setup; automatic validation and normalization of custom weights across all analysis pages.
  * **Optimization Engine:** Efficient frontier with 10,000+ Monte Carlo simulations; finds optimal portfolios by Sharpe ratio and minimum volatility.
  * **Scenario Engine:** Geometric Brownian Motion simulation (500+ paths) with percentile bands for forward portfolio valuation.
  * **Visual Outputs:** Plotly for interactive dashboards; Matplotlib/Seaborn for VaR distribution overlays; efficient frontier scatter plots.
  * **Streamlit Web App:** Interactive multi-page dashboard for real-time analysis, no coding required.

-----

## 🧠 Financial Methodology

This project applies core econometric and financial concepts:

### 1\. Logarithmic Returns

Instead of simple percentage changes, **Log Returns** are used for time-additivity and better statistical distribution (approximating Normal Distribution):
$$r_t = \ln(\frac{P_t}{P_{t-1}})$$

### 2\. Annualized Volatility (Risk)

Volatility is calculated as the rolling standard deviation of log returns. To make it comparable to industry standards (like VIX), it is annualized:
$$\sigma_{annual} = \sigma_{daily} \times \sqrt{252}$$
*(Assumption: 252 trading days in a year)*

### 3\. RSI (Relative Strength Index)

Used to measure the speed and change of price movements to identify potential reversal points.

### 4\. Modern Portfolio Theory (MPT)

Uses Mean-Variance Optimization to assess portfolio risk and return.
$$E(R_p) = \sum w_i E(R_i)$$
$$\sigma_p = \sqrt{w^T \Sigma w}$$

### 5\. Monte Carlo Simulation & Sharpe Ratio

Generates random portfolio weights to visualize the Efficient Frontier and find the maximum Sharpe ratio (Risk-Adjusted Return).
$$Sharpe = \frac{R_p - R_f}{\sigma_p}$$

### 6\. Value at Risk (VaR)

Parametric (normal) and historical simulation approaches are provided for single names and multi-asset portfolios to estimate left-tail loss at chosen confidence levels.

### 7\. Geometric Brownian Motion (GBM)

Monte Carlo forward paths ($S_t = S_{t-1} \exp((\mu - 0.5\sigma^2) + \sigma Z)$) are used to illustrate possible 1-year portfolio value envelopes.

-----

## 🛠 Tech Stack

  * **Language:** Python
  * **Data Manipulation & Stats:** Pandas, NumPy, SciPy (for parametric VaR)
  * **Data Source:** yfinance (Yahoo Finance API)
  * **Visualization:** Plotly (dashboards), Matplotlib + Seaborn (risk distributions)
  * **Environment:** Jupyter / VS Code notebooks

-----

## 💻 Installation & Usage

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/ahasdemir/Algo-Risk-Monitor.git
    cd Algo-Risk-Monitor
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit app:**

    ```bash
    streamlit run streamlit_app.py
    ```
    Open your browser to `http://localhost:8501`. Use the sidebar to navigate through:
    - **Home:** Dashboard overview
    - **Geometric Brownian Motion:** Simulate future portfolio values (500+ scenarios)
    - **Value at Risk Analysis:** Parametric & historical VaR with distribution plots
    - **Portfolio Performance:** Analyze expected returns and volatility
    - **Correlation Heatmap:** Visualize stock correlations
    - **Portfolio Optimization:** Efficient frontier and optimal allocation

4.  **Optional: Run the Jupyter notebook:**
    Open `Financial_Dashboard_Analysis.ipynb` in Jupyter Notebook or VS Code for notebook-style analysis with cell-by-cell execution.

5.  **Usage tips:**
    * Select from all 503 S&P 500 stocks in the portfolio pages.
    * Use **"Use equal weights"** checkbox for quick equal-weight portfolios.
    * Adjust **risk-free rate** in portfolio optimization to match current market conditions.
    * Tune **confidence level**, **time horizon**, and **number of simulations** for sensitivity analysis.

-----

## 🔮 Roadmap (Future Improvements)

This project is evolving into a comprehensive Risk Management Suite. Completed and upcoming features:

  - [x] **Portfolio Optimization:** Mean-Variance Analysis & Efficient Frontier.
  - [x] **Monte Carlo Simulation:** 10,000+ scenarios for optimal asset allocation.
  - [x] **GBM Forecast:** Forward valuation paths with percentile bands for portfolio scenarios.
  - [x] **Web Deployment:** Live **Streamlit** web application with interactive multi-page dashboard.
  - [ ] **Real-time Updates:** WebSocket feed for live market data (intraday VaR refresh).
  - [ ] **Backtesting Engine:** Walk-forward validation of optimal allocations.
  - [ ] **Export & Reporting:** PDF reports, Excel snapshot exports, and scheduled email alerts.
  - [ ] **Advanced Risk:** Copula models, tail hedging strategies, and stress scenario builder.

-----

## 👤 Author

**Ahmet Hasdemir**
*Economics Student | Financial Data Analyst / Jr. Data Scientist*

[LinkedIn](https://www.linkedin.com/in/ahasdemir/) | [GitHub](https://github.com/ahasdemir)