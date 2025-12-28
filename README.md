# Algo-Risk Monitor 📈

> **An automated dashboard for *monitoring* market volatility and financial risk metrics.**

  

## 📋 Executive Summary

In financial markets, price trends often mask the underlying risk. **Algo-Risk Monitor** is a quantitative analysis tool that now blends **technical momentum signals** with **multi-layered risk analytics** (parametric & historical VaR, portfolio stress tests, Monte Carlo) to turn raw market data into actionable insight.

It leverages **Logarithmic Returns** for statistical accuracy, calculates **Annualized Volatility** to standardize risk across timeframes, and layers on **RSI/SMA momentum**, **efficient frontier search**, and **scenario simulations**. The notebook produces ready-to-use visual dashboards plus exportable CSV outputs for downstream tooling.

-----

## 🚀 Key Features

  * **Automated Data Pipeline:** Pulls auto-adjusted OHLCV via `yfinance` and normalizes MultiIndex outputs.
  * **Momentum + Trend:** RSI, SMA-20/50 crossovers, and price dashboard candlesticks in Plotly.
  * **Volatility + VaR Suite:** 21-day annualized volatility, Hull-style parametric VaR, and historical VaR for both single tickers and weighted portfolios.
  * **Portfolio Analytics:** Expected returns, covariance matrix, efficient frontier exploration, and Monte Carlo search for maximum Sharpe.
  * **Screener:** BIST tickers scanner to surface the top 10 performers over a chosen window for deeper analysis.
  * **Optimization Experiments:** Minimum-risk (VaR) weight search across the "Magnificent 7" universe.
  * **Scenario Engine:** Geometric Brownian Motion simulation (500+ paths) with percentile bands for forward portfolio valuation.
  * **Visual Outputs:** Plotly for interactive dashboards; Matplotlib/Seaborn for VaR distribution overlays.

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
    cd Algo-Risk Monitor
    ```

2.  **Install dependencies:**

    ```bash
    pip install yfinance pandas numpy plotly scipy matplotlib seaborn
    ```

3.  **Run the analysis:**
    Open `Financial_Dashboard_Analysis.ipynb` in Jupyter Notebook or VS Code, select your ticker list (e.g., `GARAN.IS`, `AAPL`, `NVDA`), and run all cells. The notebook prints tail summaries, shows dashboards, and can export CSVs (e.g., `TSLA_volatility_analysis.csv`).

4.  **Optional workflows:**
    * Switch `period` arguments (e.g., `10y`) for longer histories.
    * Use the BIST screener to identify the top performers and feed them into the portfolio simulations.
    * Adjust `num_portfolios` or `simulations` to trade off speed vs. scenario coverage.

-----

## 🔮 Roadmap (Future Improvements)

This project is evolving into a comprehensive Risk Management Suite. Upcoming modules:

  - [x] **Portfolio Optimization:** Mean-Variance Analysis & Efficient Frontier.
  - [x] **Monte Carlo Simulation:** 10,000+ scenarios for optimal asset allocation.
  - [ ] **Correlation Matrix:** Detecting cross-asset dependencies (Heatmap).
  - [ ] **Beta Calculation:** Measuring systematic risk against benchmark indices (S\&P 500 / BIST 100).
  - [ ] **Credit Risk Modeling:** Implementing Machine Learning classifiers for credit scoring.
  - [ ] **Web Deployment:** Converting the notebook into a live **Streamlit** web application.

-----

## 👤 Author

**Ahmet Hasdemir**
*Economics Student | Financial Data Analyst / Jr. Data Scientist*

[LinkedIn](https://www.linkedin.com/in/ahasdemir/) | [GitHub](https://github.com/ahasdemir)