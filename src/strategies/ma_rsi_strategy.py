"""
Project: NIFTY 50 Historical Data Analysis
Module: MA + RSI Trading Strategy
Purpose: Generate bullish and bearish trading signals.
"""

import pandas as pd
from pathlib import Path

# 1. Define project directories

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nifty50_indicators.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nifty50_strategy_signals.csv"
)



# 2. Load historical indicator data

df = pd.read_csv(DATA_FILE, index_col=0, parse_dates=True)

print("Dataset loaded successfully!")

print("Total records:", len(df))

print("\nAvailable columns:")
print(df.columns.tolist())



# 3. Validate required columns

required_columns = [
    "Close",
    "SMA_20",
    "SMA_50",
    "RSI"
]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Missing required column: {column}")

print("\nAll required columns are available!") 



# 4. Generate trading signals

df["Previous_SMA_20"] = df["SMA_20"].shift(1)
df["Previous_SMA_50"] = df["SMA_50"].shift(1)

df["Signal"] = "NO TRADE"

# Bullish crossover
bullish = (
    (df["Previous_SMA_20"] <= df["Previous_SMA_50"]) &
    (df["SMA_20"] > df["SMA_50"]) &
    (df["RSI"] > 50)
)

# Bearish crossover
bearish = (
    (df["Previous_SMA_20"] >= df["Previous_SMA_50"]) &
    (df["SMA_20"] < df["SMA_50"]) &
    (df["RSI"] < 50)
)

df.loc[bullish, "Signal"] = "BUY CE"
df.loc[bearish, "Signal"] = "BUY PE"

print("\nTrading signals generated!")
print(df["Signal"].value_counts()) 

print("Total signal records:", df["Signal"].count())
print("Total DataFrame records:", len(df))



# 5. Save strategy results

df.to_csv(OUTPUT_FILE, index_label="Date")

print("\nStrategy results saved successfully!")
print("Saved file:", OUTPUT_FILE)



