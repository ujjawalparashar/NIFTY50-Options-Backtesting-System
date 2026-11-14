
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# 1. Project directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# 2. Dataset paths
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "nifty50_backtest_results.csv"

# 3. Page configuration
st.set_page_config(
    page_title="NIFTY 50 Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)

# 4. Dashboard heading
st.title("NIFTY 50 Historical Data Analysis")
st.subheader("Technical Indicators and Strategy Backtesting")
st.caption("Historical index analysis | MA20 + MA50 + RSI strategy")

# 5. Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE, parse_dates=["Date"])
    df = df.sort_values("Date")
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error(f"Dataset not found: {DATA_FILE}")
    st.stop()

# 6. Sidebar filters
st.sidebar.header("Dashboard Filters")

start_date = st.sidebar.date_input(
    "Start date",
    value=df["Date"].min().date()
)

end_date = st.sidebar.date_input(
    "End date",
    value=df["Date"].max().date()
)

if start_date > end_date:
    st.error("Start date cannot be after end date.")
    st.stop()

filtered_df = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date)
].copy()

if filtered_df.empty:
    st.warning("No data available for the selected dates.")
    st.stop()

# 7. Key performance indicators
st.header("Market and Strategy Overview")

latest = filtered_df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Latest NIFTY 50 Close", f"{latest['Close']:,.2f}")
col2.metric("Latest RSI", f"{latest['RSI']:.2f}")
col3.metric("Trading Signal", str(latest["Signal"]))
col4.metric("Strategy Return", f"{(latest['Cumulative_Strategy_Return'] - 1) * 100:.2f}%")

# 8. NIFTY 50 price chart
st.header("NIFTY 50 Price and Moving Averages")

fig_price = px.line(
    filtered_df,
    x="Date",
    y=["Close", "SMA_20", "SMA_50"],
    title="NIFTY 50 with 20-day and 50-day Moving Averages"
)

st.plotly_chart(fig_price, use_container_width=True)

# 9. RSI chart
st.header("Relative Strength Index (RSI)")

fig_rsi = px.line(
    filtered_df,
    x="Date",
    y="RSI",
    title="RSI Indicator"
)

fig_rsi.add_hline(y=70, line_dash="dash")
fig_rsi.add_hline(y=30, line_dash="dash")

st.plotly_chart(fig_rsi, use_container_width=True)

# 10. Strategy performance chart
st.header("Strategy Performance vs NIFTY 50")

fig_returns = px.line(
    filtered_df,
    x="Date",
    y=["Cumulative_Strategy_Return", "Cumulative_Benchmark"],
    title="Cumulative Strategy Return vs Buy and Hold"
)

st.plotly_chart(fig_returns, use_container_width=True)

# 11. Drawdown chart
st.header("Strategy Drawdown")

fig_drawdown = px.line(
    filtered_df,
    x="Date",
    y="Drawdown",
    title="Historical Strategy Drawdown"
)

st.plotly_chart(fig_drawdown, use_container_width=True)

# 12. Trading signals
st.header("Trading Signals")

signals = filtered_df[
    filtered_df["Signal"].isin(["BUY CE", "BUY PE"])
][["Date", "Close", "RSI", "Signal"]]

st.dataframe(signals.tail(20), use_container_width=True)

# 13. Historical data table
st.header("Historical Dataset")

st.dataframe(filtered_df.tail(50), use_container_width=True)

# 14. Download filtered dataset
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data",
    data=csv_data,
    file_name="nifty50_analysis.csv",
    mime="text/csv"
)

st.caption(
    "Educational research project. Backtesting uses NIFTY 50 index returns, "
    "not actual historical CE/PE option premiums."
)

st.success("Dashboard loaded successfully!")



