
"""
Project: NIFTY 50 Historical Data Analysis
Module: Technical Indicators
Purpose: Calculate RSI, MACD, Bollinger Bands,
ATR and Historical Volatility.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Project directories
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = PROJECT_ROOT / "data" / "processed" / "nifty50_clean.csv"

OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "nifty50_indicators.csv"

FIGURE_DIR = PROJECT_ROOT / "reports" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# 2. Load historical data
df = pd.read_csv(DATA_FILE, header=[0, 1], index_col=0)

# Flatten Yahoo Finance multi-level columns
df.columns = df.columns.get_level_values(0)

df.index = pd.to_datetime(df.index)

df = df.sort_index()

# 3. Calculate daily returns
df["Daily_Return"] = df["Close"].pct_change()

# 4. Calculate RSI (14 days)
delta = df["Close"].diff()

gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.ewm(
    alpha=1/14, min_periods=14, adjust=False
).mean()

avg_loss = loss.ewm(
    alpha=1/14, min_periods=14, adjust=False
).mean()

rs = avg_gain / avg_loss

df["RSI"] = 100 - (100 / (1 + rs))

# 5. Calculate MACD
ema_12 = df["Close"].ewm(span=12, adjust=False).mean()
ema_26 = df["Close"].ewm(span=26, adjust=False).mean()

df["MACD"] = ema_12 - ema_26

df["MACD_Signal"] = df["MACD"].ewm(
    span=9, adjust=False
).mean()

df["MACD_Histogram"] = df["MACD"] - df["MACD_Signal"]

# 6. Calculate Bollinger Bands (20 days)
df["SMA_20"] = df["Close"].rolling(20).mean()
df["SMA_50"] = df["Close"].rolling(50).mean()

rolling_std = df["Close"].rolling(20).std()

df["Upper_Band"] = df["SMA_20"] + (2 * rolling_std)

df["Lower_Band"] = df["SMA_20"] - (2 * rolling_std)

# 7. Calculate ATR (14 days)
previous_close = df["Close"].shift(1)

true_range = pd.concat(
    [
        df["High"] - df["Low"],
        (df["High"] - previous_close).abs(),
        (df["Low"] - previous_close).abs()
    ],
    axis=1
).max(axis=1)

df["ATR"] = true_range.ewm(
    alpha=1/14, min_periods=14, adjust=False
).mean()

# 8. Calculate Historical Volatility (20 days)
df["Historical_Volatility"] = (
    df["Daily_Return"].rolling(20).std()
    * np.sqrt(252) * 100
)

# 9. Save calculated indicators
df.to_csv(OUTPUT_FILE)

# 10. Display results
print("\nTECHNICAL INDICATORS CALCULATED")
print("--------------------------------")

print("Total records:", len(df))

print("\nLatest indicator values:")

print(df[
    [
        "Close",
        "RSI",
        "MACD",
        "MACD_Signal",
        "Upper_Band",
        "Lower_Band",
        "ATR",
        "Historical_Volatility"
    ]
].tail())

print("\nMissing values:")
print(df.isnull().sum())

print("\nSaved file:")
print(OUTPUT_FILE)

# 11. Plot technical indicators
fig, axes = plt.subplots(3, 1, figsize=(15, 12))

# Price and Bollinger Bands
axes[0].plot(df.index, df["Close"], label="NIFTY 50")
axes[0].plot(df.index, df["Upper_Band"], label="Upper Band")
axes[0].plot(df.index, df["Lower_Band"], label="Lower Band")
axes[0].set_title("NIFTY 50 Bollinger Bands")
axes[0].legend()
axes[0].grid(True)

# RSI
axes[1].plot(df.index, df["RSI"], label="RSI")
axes[1].axhline(70, linestyle="--")
axes[1].axhline(30, linestyle="--")
axes[1].set_title("Relative Strength Index (RSI)")
axes[1].legend()
axes[1].grid(True)

# MACD
axes[2].plot(df.index, df["MACD"], label="MACD")
axes[2].plot(df.index, df["MACD_Signal"], label="Signal")
axes[2].set_title("MACD Indicator")
axes[2].legend()
axes[2].grid(True)

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "technical_indicators.png",
    dpi=300
)

plt.show()

print("\nTECHNICAL INDICATOR ANALYSIS COMPLETED!")
