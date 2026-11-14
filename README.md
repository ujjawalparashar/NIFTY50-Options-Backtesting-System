
# NIFTY 50 Historical Data Analysis and Options Strategy Backtesting System

## 1. Project Overview

The NIFTY 50 Historical Data Analysis and Options Strategy Backtesting System is a Python-based analytical application developed to study historical NIFTY 50 market data, calculate technical indicators, generate trading signals, and evaluate a rule-based trading strategy through historical backtesting.

The project also provides an interactive dashboard built using Streamlit to visualize market trends, technical indicators, trading signals, and backtesting results.

## 2. Objectives

- Collect and analyze historical NIFTY 50 data.
- Perform data cleaning and preprocessing.
- Calculate technical indicators.
- Generate rule-based bullish and bearish trading signals.
- Backtest the trading strategy using historical data.
- Visualize analytical results through an interactive dashboard.

## 3. Key Features

- Historical NIFTY 50 data analysis
- Data preprocessing and cleaning
- Moving Average (SMA 20 and SMA 50)
- Relative Strength Index (RSI)
- Moving Average Convergence Divergence (MACD)
- Bollinger Bands
- Average True Range (ATR)
- Rule-based BUY CE and BUY PE signals
- Strategy performance evaluation
- Cumulative returns and drawdown analysis
- Interactive Streamlit dashboard
- Historical data visualization and CSV export

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Pandas | Data manipulation |
| NumPy | Numerical computation |
| Matplotlib | Data visualization |
| Plotly | Interactive charts |
| Streamlit | Dashboard development |
| yfinance | Historical market data |
| VS Code | Development environment |
| Git and GitHub | Version control |

## 5. Project Structure

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
└── .gitignore
```

## 6. Methodology

The project follows these major stages:

1. Historical Data Collection
2. Data Verification and Preprocessing
3. Exploratory Data Analysis
4. Technical Indicator Calculation
5. Trading Signal Generation
6. Strategy Backtesting
7. Performance Evaluation
8. Dashboard Visualization

## 7. Trading Strategy

The system uses Simple Moving Average crossover conditions along with RSI confirmation to generate trading signals.

- BUY CE: Bullish SMA crossover with RSI confirmation.
- BUY PE: Bearish SMA crossover with RSI confirmation.
- NO TRADE: When the specified conditions are not satisfied.

## 8. Backtesting

The strategy is evaluated using historical NIFTY 50 index data. The backtesting module calculates strategy returns, cumulative returns, winning and losing sessions, win rate, and drawdown.

**Important:** The current implementation uses NIFTY 50 index price movements as a proxy for bullish and bearish CE/PE-style signals. It does not yet calculate actual options contract premiums, expiry effects, or options trading P&L.

## 9. Installation and Execution

Clone the repository:

```bash
git clone https://github.com/ujjawalparashar/NIFTY50-Options-Backtesting-System.git
```

Move into the project directory:

```bash
cd NIFTY50-Options-Backtesting-System
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

## 10. Future Scope

- Integration of historical NIFTY options contract data.
- Actual options premium-based backtesting.
- Expiry and strike-price selection.
- Brokerage and transaction cost calculations.
- Advanced options trading strategies.
- Enhanced risk management and performance metrics.

## 11. Disclaimer

This project is developed for academic and educational purposes only. The analysis and backtesting results are based on historical data and do not constitute investment advice or a recommendation to trade.

## 12. Author

**Ujjawal Parashar**

MCA Student

GitHub: https://github.com/ujjawalparashar

---

**Project:** NIFTY 50 Historical Data Analysis and Options Strategy Backtesting System

## Dashboard Screenshots

[View Project Dashboard Screenshots (PDF)](dashboard_screenshots.pdf)
