# NIFTY 50 Historical Data Analysis and Options Strategy Backtesting System

## 1. Project Overview

The **NIFTY 50 Historical Data Analysis and Options Strategy Backtesting System** is a Python-based project developed to analyse historical NIFTY 50 market data, calculate technical indicators, generate trading signals, and evaluate a rule-based trading strategy through historical backtesting.

The project provides an interactive dashboard built using Streamlit to visualise market trends, technical indicators, trading signals, and backtesting performance.

## 2. Objectives

- Analyse historical NIFTY 50 index data.
- Perform data cleaning and preprocessing.
- Calculate technical indicators such as SMA, RSI, MACD, Bollinger Bands and ATR.
- Generate bullish and bearish trading signals.
- Backtest a rule-based trading strategy.
- Evaluate strategy returns and drawdown.
- Present results through an interactive dashboard.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Pandas | Data manipulation |
| NumPy | Numerical calculations |
| Matplotlib | Data visualisation |
| Plotly | Interactive charts |
| Streamlit | Dashboard development |
| yfinance | Historical market data retrieval |
| SciPy | Scientific calculations |
| Git & GitHub | Version control |

## 4. System Workflow

1. Historical NIFTY 50 data collection
2. Data verification and preprocessing
3. Exploratory data analysis
4. Technical indicator calculation
5. Trading signal generation
6. Strategy backtesting
7. Performance evaluation
8. Interactive dashboard visualisation

## 5. Technical Indicators

The project calculates the following indicators:

- Simple Moving Average (SMA 20 and SMA 50)
- Relative Strength Index (RSI)
- Moving Average Convergence Divergence (MACD)
- Bollinger Bands
- Average True Range (ATR)
- Historical Volatility

## 6. Trading Strategy

The implemented strategy uses moving-average crossover conditions combined with RSI confirmation.

- **BUY CE:** Bullish moving-average crossover with RSI confirmation.
- **BUY PE:** Bearish moving-average crossover with RSI confirmation.
- **NO TRADE:** When the entry conditions are not satisfied.

## 7. Backtesting

The system evaluates historical strategy signals using subsequent-session index returns.

Performance measures include:

- Total strategy return
- Win rate
- Winning and losing sessions
- Cumulative returns
- Maximum drawdown
- Benchmark comparison

**Important scope note:** The current implementation uses NIFTY 50 index movements as a proxy for bullish and bearish CE/PE-style signals. It does not yet calculate actual options-contract premiums, brokerage, or options trading P&L.

## 8. Interactive Dashboard

The Streamlit dashboard provides:

- Key performance indicators
- NIFTY 50 historical price charts
- Moving-average visualisation
- RSI analysis
- Cumulative strategy and benchmark returns
- Drawdown analysis
- Trading signal history
- Historical data table
- CSV download functionality

## 9. Project Structure

```text
NIFTY50_Options_Backtesting/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── reports/
│   └── figures/
│
├── src/
│   ├── analysis/
│   ├── backtesting/
│   ├── data_collection/
│   ├── preprocessing/
│   └── strategies/
│
├── tests/
├── documentation/
├── models/
├── notebooks/
├── requirements.txt
└── README.md
```

## 10. Installation and Execution

### Step 1: Clone the repository

```bash
git clone https://github.com/ujjawalparashar/NIFTY50-Options-Backtesting-System.git
```

### Step 2: Open the project directory

```bash
cd NIFTY50-Options-Backtesting-System
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

### Step 4: Activate the environment (Windows)

```powershell
.venv\Scripts\activate
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Launch the dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will open in your default web browser.

## 11. Data Source

Historical NIFTY 50 index data was retrieved using Yahoo Finance through the `yfinance` Python library.

The dataset is used for academic analysis and strategy backtesting.

## 12. Project Screenshots

[View Project Dashboard Screenshots (PDF)](dashboard_screenshots.pdf)

## 13. Limitations

- The current backtesting engine uses index-based returns rather than actual options-contract prices.
- Transaction costs, slippage and brokerage are not included.
- Historical performance does not guarantee future results.
- The historical dataset depends on the availability and accuracy of the external data source.

## 14. Future Scope

- Integration of historical NIFTY options-chain data.
- Actual CE and PE premium-based backtesting.
- Inclusion of brokerage, slippage and transaction costs.
- Additional options strategies.
- Advanced risk and performance metrics.
- Improved dashboard functionality.

## 15. Disclaimer

This project has been developed for academic and educational purposes only. It is not intended to provide investment advice or live trading recommendations.

---

**Developed as an MCA Minor Project.**

**GitHub Repository:**  
https://github.com/ujjawalparashar/NIFTY50-Options-Backtesting-System
