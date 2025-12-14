# Algo-Risk Monitor 📈

> **An automated dashboard for *monitoring* market volatility and financial risk metrics.**

  

## 📋 Executive Summary

In financial markets, price trends often mask the underlying risk. **Algo-Risk Monitor** is a quantitative analysis tool designed to bridge the gap between raw market data and actionable risk insights.

Unlike standard price trackers, this project focuses on **volatility clustering** and **momentum**, providing a comprehensive view of an asset's risk profile. It leverages **Logarithmic Returns** for statistical accuracy and calculates **Annualized Volatility** to standardize risk assessment across different timeframes.

This dashboard serves as a decision-support tool for traders and risk analysts, enabling them to identify **"High Risk / Low Reward"** zones instantly.

-----

## 🚀 Key Features

  * **Automated Data Pipeline:** Fetches real-time OHLCV (Open, High, Low, Close, Volume) data using `yfinance` API (Auto-adjusted for splits/dividends).
  * **Dynamic Volatility Analysis:** Calculates 21-day rolling standard deviation, annualized ($\sigma \times \sqrt{252}$) to measure market risk.
  * **Momentum Tracking:** Integrated **RSI (Relative Strength Index)** to detect Overbought (\>70) and Oversold (\<30) conditions.
  * **Trend Identification:** Uses SMA (Simple Moving Averages) crossover logic (SMA 20 vs SMA 50).
  * **Portfolio Optimization:** Analyzes multiple assets to calculate Expected Returns and Covariance Matrix.
  * **Top Performers Scanner:** Automatically identifies top-performing stocks from a given list (e.g., BIST 30) over a specified period.
  * **Monte Carlo Simulation:** Simulates 10,000+ portfolio combinations to identify the Optimal Portfolio based on the Sharpe Ratio (Efficient Frontier).
  * **Professional Visualization:** Interactive **Plotly** charts with removed non-trading days (weekends) for a seamless analytical experience.

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

-----

## 🛠 Tech Stack

  * **Language:** Python
  * **Data Manipulation:** Pandas, NumPy
  * **Data Source:** yfinance (Yahoo Finance API)
  * **Visualization:** Plotly Graph Objects, Plotly Subplots

-----

## 💻 Installation & Usage

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/ahasdemir/Algo-Risk-Monitor.git
    cd Algo-Risk Monitor
    ```

2.  **Install dependencies:**

    ```bash
    pip install yfinance pandas numpy plotly
    ```

3.  **Run the analysis:**
    Open `Financial_Dashboard_Analysis.ipynb` in Jupyter Notebook or VS Code and run all cells.

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