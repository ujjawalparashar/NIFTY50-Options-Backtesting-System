from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# NIFTY 50 ANALYTICS DASHBOARD


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "nifty50_backtest_results.csv"

st.set_page_config(
    page_title="NIFTY 50 | Analytics Terminal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------- Styling ----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp {
        background:
            radial-gradient(circle at 8% 0%, rgba(37,99,235,.16), transparent 28%),
            radial-gradient(circle at 92% 8%, rgba(124,58,237,.13), transparent 25%),
            #080f1e;
        color: #e8eefc;
    }
    [data-testid="stHeader"] { background: rgba(8,15,30,.75); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #101b31 0%, #0b1426 100%);
        border-right: 1px solid rgba(148,163,184,.16);
    }
    [data-testid="stSidebar"] * { color: #e6edff; }
    .hero {
        padding: 26px 30px 24px 30px;
        border: 1px solid rgba(125,155,220,.24);
        border-radius: 22px;
        background: linear-gradient(115deg, rgba(20,43,82,.96), rgba(36,30,76,.92));
        box-shadow: 0 18px 50px rgba(0,0,0,.22);
        margin-bottom: 22px;
    }
    .hero-kicker {
        color: #8fb8ff; text-transform: uppercase; letter-spacing: 2px;
        font-size: 11px; font-weight: 800;
    }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif; font-size: 34px;
        font-weight: 700; color: #ffffff; line-height: 1.15; margin: 8px 0;
    }
    .hero-sub { color: #c3d2ef; font-size: 14px; }
    .section-label {
        color: #9bbcff; font-size: 12px; font-weight: 800;
        text-transform: uppercase; letter-spacing: 1.5px;
        margin: 10px 0 12px 0;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(23,39,67,.98), rgba(17,28,49,.98));
        border: 1px solid rgba(125,155,220,.20);
        padding: 17px 18px; border-radius: 16px;
        box-shadow: 0 10px 24px rgba(0,0,0,.13);
    }
    div[data-testid="stMetricLabel"] { color: #a9bbd9 !important; }
    div[data-testid="stMetricValue"] { color: #f7faff !important; font-family: 'Space Grotesk'; }
    div[data-testid="stMetricDelta"] { font-weight: 700; }
    .panel {
        border: 1px solid rgba(125,155,220,.18);
        background: rgba(17,29,51,.76); border-radius: 16px;
        padding: 15px 18px; margin: 8px 0 16px 0;
    }
    .pill {
        display: inline-block; padding: 5px 11px; border-radius: 30px;
        background: rgba(59,130,246,.16); color: #9fc5ff;
        border: 1px solid rgba(96,165,250,.28); font-size: 11px;
        font-weight: 700; margin-right: 6px;
    }
    .small-note { color: #91a4c3; font-size: 12px; }
    div.stButton > button, div.stDownloadButton > button {
        border-radius: 10px; border: 1px solid rgba(96,165,250,.4);
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        color: white; font-weight: 700;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        border-color: #bfdbfe; color: white;
    }
    .stTabs [data-baseweb="tab"] { color: #b9c9e5; font-weight: 700; }
    .stTabs [aria-selected="true"] { color: #8bb8ff !important; }
    [data-testid="stDataFrame"] { border: 1px solid rgba(125,155,220,.18); border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------- Data ----------------------------
@st.cache_data
def load_data():
    data = pd.read_csv(DATA_FILE, parse_dates=["Date"])
    data = data.sort_values("Date").reset_index(drop=True)
    return data


if not DATA_FILE.exists():
    st.error(f"Dataset not found: {DATA_FILE}")
    st.info("Please make sure the backtest results CSV is present in data/processed/.")
    st.stop()

try:
    df = load_data()
except Exception as exc:
    st.error(f"Could not load the project dataset: {exc}")
    st.stop()

required = ["Date", "Close", "Signal"]
missing = [col for col in required if col not in df.columns]
if missing:
    st.error(f"The dataset is missing required columns: {', '.join(missing)}")
    st.stop()

# ---------------------------- Sidebar ----------------------------
st.sidebar.markdown("## 🎛️ Control Centre")
st.sidebar.caption("Explore the historical dataset")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

quick_period = st.sidebar.selectbox(
    "Quick date range",
    ["Full history", "Last 1 year", "Last 3 years", "Last 5 years", "Custom"],
    index=0,
)

if quick_period == "Last 1 year":
    default_start = max(df["Date"].min(), df["Date"].max() - pd.DateOffset(years=1)).date()
elif quick_period == "Last 3 years":
    default_start = max(df["Date"].min(), df["Date"].max() - pd.DateOffset(years=3)).date()
elif quick_period == "Last 5 years":
    default_start = max(df["Date"].min(), df["Date"].max() - pd.DateOffset(years=5)).date()
else:
    default_start = min_date

if quick_period == "Custom":
    start_date = st.sidebar.date_input("Start date", value=default_start, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("End date", value=max_date, min_value=min_date, max_value=max_date)
else:
    start_date, end_date = default_start, max_date

if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Chart controls")
show_sma20 = st.sidebar.checkbox("Show SMA 20", value=True)
show_sma50 = st.sidebar.checkbox("Show SMA 50", value=True)
show_volume = st.sidebar.checkbox("Show volume (if available)", value=False)
chart_style = st.sidebar.radio("Chart style", ["Line", "Candlestick"], horizontal=False)
st.sidebar.markdown("---")
signal_filter = st.sidebar.multiselect(
    "Trading signal filter",
    options=["BUY CE", "BUY PE", "NO TRADE"],
    default=["BUY CE", "BUY PE", "NO TRADE"],
)
table_rows = st.sidebar.select_slider("Rows in data explorer", options=[10, 25, 50, 100, 250], value=50)

filtered = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date)
].copy()

if filtered.empty:
    st.warning("No records found for the selected date range.")
    st.stop()

# ---------------------------- Header ----------------------------
st.markdown(
    """
    <div class="hero">
      <div class="hero-kicker">Market intelligence • Historical research</div>
      <div class="hero-title">NIFTY 50 Analytics Terminal</div>
      <div class="hero-sub">Historical price analysis, technical indicators, trading signals and strategy backtesting</div>
      <div style="margin-top:14px">
        <span class="pill">MA 20 / MA 50</span>
        <span class="pill">RSI</span>
        <span class="pill">Strategy Backtest</span>
        <span class="pill">Interactive Explorer</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

latest = filtered.iloc[-1]
first = filtered.iloc[0]
price_change = ((latest["Close"] / first["Close"]) - 1) * 100 if first["Close"] else 0
strategy_return = (latest["Cumulative_Strategy_Return"] - 1) * 100 if "Cumulative_Strategy_Return" in filtered else None
benchmark_return = (latest["Cumulative_Benchmark"] - 1) * 100 if "Cumulative_Benchmark" in filtered else None
latest_rsi = latest.get("RSI", None)
latest_signal = str(latest["Signal"])

st.markdown('<div class="section-label">▰ Market snapshot</div>', unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("NIFTY 50 Close", f"{latest['Close']:,.2f}", f"{price_change:+.2f}% in selected period")
k2.metric("RSI (latest)", f"{latest_rsi:.2f}" if pd.notna(latest_rsi) else "N/A")
k3.metric("Latest Signal", latest_signal)
k4.metric("Strategy Return", f"{strategy_return:+.2f}%" if strategy_return is not None else "N/A")
k5.metric("Benchmark Return", f"{benchmark_return:+.2f}%" if benchmark_return is not None else "N/A")

st.caption(f"Showing {len(filtered):,} trading sessions from {filtered['Date'].min():%d %b %Y} to {filtered['Date'].max():%d %b %Y}.")

# ---------------------------- Tabs ----------------------------
tab_overview, tab_technical, tab_signals, tab_backtest, tab_data = st.tabs(
    ["🏠 Overview", "📉 Technical Analysis", "⚡ Trading Signals", "🧪 Backtesting", "🗂️ Data Explorer"]
)

# Shared Plotly theme
plot_layout = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(12,22,40,.55)",
    font=dict(color="#dce7fa", family="DM Sans"),
    margin=dict(l=15, r=15, t=55, b=15),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

with tab_overview:
    st.markdown('<div class="section-label">▰ Price movement</div>', unsafe_allow_html=True)
    if chart_style == "Candlestick" and all(c in filtered.columns for c in ["Open", "High", "Low", "Close"]):
        fig = go.Figure(data=[go.Candlestick(
            x=filtered["Date"], open=filtered["Open"], high=filtered["High"],
            low=filtered["Low"], close=filtered["Close"], name="NIFTY 50"
        )])
        if show_sma20 and "SMA_20" in filtered:
            fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["SMA_20"], name="SMA 20", line=dict(width=2, color="#38bdf8")))
        if show_sma50 and "SMA_50" in filtered:
            fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["SMA_50"], name="SMA 50", line=dict(width=2, color="#c084fc")))
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["Close"], name="Close", line=dict(color="#60a5fa", width=2.5)))
        if show_sma20 and "SMA_20" in filtered:
            fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["SMA_20"], name="SMA 20", line=dict(color="#34d399", width=1.8)))
        if show_sma50 and "SMA_50" in filtered:
            fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["SMA_50"], name="SMA 50", line=dict(color="#c084fc", width=1.8)))
    fig.update_layout(title="NIFTY 50 • Price & Moving Averages", xaxis_title="", yaxis_title="Index level", **plot_layout)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(148,163,184,.12)")
    st.plotly_chart(fig, use_container_width=True)

    if show_volume and "Volume" in filtered.columns:
        volume_fig = px.bar(filtered, x="Date", y="Volume", title="Trading Volume")
        volume_fig.update_layout(**plot_layout)
        st.plotly_chart(volume_fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        if "RSI" in filtered.columns:
            rsi_fig = go.Figure()
            rsi_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["RSI"], name="RSI", line=dict(color="#fbbf24", width=2)))
            rsi_fig.add_hline(y=70, line_dash="dash", line_color="#fb7185", annotation_text="Overbought 70")
            rsi_fig.add_hline(y=30, line_dash="dash", line_color="#34d399", annotation_text="Oversold 30")
            rsi_fig.update_layout(title="RSI Momentum", yaxis_title="RSI", **plot_layout)
            st.plotly_chart(rsi_fig, use_container_width=True)
    with right:
        signal_counts = filtered["Signal"].value_counts().reindex(["BUY CE", "BUY PE", "NO TRADE"]).fillna(0).astype(int).reset_index()
        signal_counts.columns = ["Signal", "Sessions"]
        sig_fig = px.pie(signal_counts, names="Signal", values="Sessions", hole=0.62,
                         title="Signal Distribution", color="Signal",
                         color_discrete_map={"BUY CE": "#22c55e", "BUY PE": "#f97316", "NO TRADE": "#64748b"})
        sig_fig.update_layout(**plot_layout)
        st.plotly_chart(sig_fig, use_container_width=True)

with tab_technical:
    st.markdown('<div class="section-label">▰ Technical indicator workspace</div>', unsafe_allow_html=True)
    indicator_options = [c for c in ["RSI", "SMA_20", "SMA_50", "MACD", "MACD_Signal", "Upper_Band", "Lower_Band", "ATR", "Historical_Volatility"] if c in filtered.columns]
    selected_indicators = st.multiselect("Choose indicators to plot", indicator_options, default=[c for c in ["RSI", "SMA_20", "SMA_50"] if c in indicator_options])
    if selected_indicators:
        tech_fig = go.Figure()
        for col in selected_indicators:
            tech_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered[col], name=col, mode="lines"))
        tech_fig.update_layout(title="Selected Technical Indicators", xaxis_title="", yaxis_title="Indicator value", **plot_layout)
        st.plotly_chart(tech_fig, use_container_width=True)
    else:
        st.info("Select one or more indicators above to display the chart.")

    summary_cols = [c for c in ["Close", "SMA_20", "SMA_50", "RSI", "MACD", "ATR", "Historical_Volatility"] if c in filtered.columns]
    if summary_cols:
        st.markdown("#### Latest indicator readings")
        st.dataframe(filtered[["Date"] + summary_cols].tail(1), use_container_width=True, hide_index=True)

with tab_signals:
    st.markdown('<div class="section-label">▰ Signal monitor</div>', unsafe_allow_html=True)
    signal_view = filtered[filtered["Signal"].isin(signal_filter)].copy()
    signal_only = signal_view[signal_view["Signal"].isin(["BUY CE", "BUY PE"])]
    a, b, c = st.columns(3)
    a.metric("BUY CE", int((signal_view["Signal"] == "BUY CE").sum()))
    b.metric("BUY PE", int((signal_view["Signal"] == "BUY PE").sum()))
    c.metric("All displayed rows", f"{len(signal_view):,}")
    display_cols = [c for c in ["Date", "Open", "High", "Low", "Close", "RSI", "Signal", "Strategy_Return"] if c in signal_view.columns]
    st.markdown("#### All selected signals")
    st.dataframe(signal_view[display_cols].sort_values("Date", ascending=False), use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Download signal data (CSV)",
        data=signal_view.to_csv(index=False).encode("utf-8"),
        file_name="nifty50_trading_signals.csv",
        mime="text/csv",
    )

with tab_backtest:
    st.markdown('<div class="section-label">▰ Backtesting performance lab</div>', unsafe_allow_html=True)
    if "Cumulative_Strategy_Return" in filtered.columns and "Cumulative_Benchmark" in filtered.columns:
        perf_fig = go.Figure()
        perf_fig.add_trace(go.Scatter(x=filtered["Date"], y=(filtered["Cumulative_Strategy_Return"] - 1) * 100,
                                      name="Strategy", line=dict(color="#a78bfa", width=2.5)))
        perf_fig.add_trace(go.Scatter(x=filtered["Date"], y=(filtered["Cumulative_Benchmark"] - 1) * 100,
                                      name="NIFTY 50 Buy & Hold", line=dict(color="#38bdf8", width=2.5)))
        perf_fig.update_layout(title="Cumulative Return Comparison", xaxis_title="", yaxis_title="Return (%)", **plot_layout)
        st.plotly_chart(perf_fig, use_container_width=True)
    if "Drawdown" in filtered.columns:
        dd_fig = px.area(filtered, x="Date", y="Drawdown", title="Strategy Drawdown")
        dd_fig.update_traces(line_color="#fb7185", fillcolor="rgba(251,113,133,.20)")
        dd_fig.update_layout(yaxis_title="Drawdown", xaxis_title="", **plot_layout)
        st.plotly_chart(dd_fig, use_container_width=True)

    perf1, perf2, perf3 = st.columns(3)
    if "Strategy_Return" in filtered.columns:
        active = filtered[filtered["Strategy_Return"].fillna(0) != 0]
        wins = int((active["Strategy_Return"] > 0).sum())
        losses = int((active["Strategy_Return"] < 0).sum())
        win_rate = (wins / len(active) * 100) if len(active) else 0
        perf1.metric("Active sessions", f"{len(active):,}")
        perf2.metric("Winning sessions", f"{wins:,}")
        perf3.metric("Win rate", f"{win_rate:.2f}%")

    st.info("Interpretation note: this project backtests directional signals using NIFTY 50 index returns. It does not calculate actual historical CE/PE option-premium P&L.")

with tab_data:
    st.markdown('<div class="section-label">▰ Historical data explorer</div>', unsafe_allow_html=True)
    available_columns = list(filtered.columns)
    chosen_columns = st.multiselect("Choose columns to display", available_columns, default=available_columns)
    if chosen_columns:
        st.dataframe(filtered[chosen_columns].tail(table_rows), use_container_width=True, hide_index=True)
    else:
        st.warning("Choose at least one column to display.")
    st.download_button(
        "⬇️ Download filtered historical dataset",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="nifty50_filtered_historical_data.csv",
        mime="text/csv",
    )

# ---------------------------- Footer ----------------------------
st.markdown("---")
st.markdown(
    """
    <div class="small-note">
    <b>Academic project disclaimer:</b> For educational and research purposes only.
    Strategy signals are based on NIFTY 50 index data and are not a representation
    of actual options-contract execution, premiums, brokerage, slippage or taxes.
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("NIFTY 50 Analytics Terminal • Interactive dashboard")
