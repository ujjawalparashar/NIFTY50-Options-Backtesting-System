"""
Project: NIFTY 50 Historical Data Analysis
Module: Index Signal Backtesting
Purpose: Evaluate historical performance of MA20 + MA50 + RSI strategy.
"""

import pandas as pd
import numpy as np
from pathlib import Path


# 1. Define project directories

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nifty50_strategy_signals.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nifty50_backtest_results.csv"
)



# 2. Load strategy signals

df = pd.read_csv(INPUT_FILE, index_col=0, parse_dates=True)

print("Strategy data loaded successfully!")
print("Total records:", len(df))

print("\nAvailable columns:")
print(df.columns.tolist())



# 3. Convert trading signals into positions

df["Position"] = 0

df.loc[df["Signal"] == "BUY CE", "Position"] = 1

df.loc[df["Signal"] == "BUY PE", "Position"] = -1

# 4. Calculate trading session return
df["Session_Return"] = (
    (df["Close"] / df["Open"]) - 1
)

# 5. Apply previous day's signal to current session return
df["Strategy_Return"] = (
    df["Position"].shift(1) * df["Session_Return"]
)

print("\nReturn calculations completed!")
print(df[["Signal", "Position", "Session_Return", "Strategy_Return"]].tail(10)) 



# 6. Calculate cumulative returns

df["Strategy_Return"] = df["Strategy_Return"].fillna(0)

df["Cumulative_Strategy_Return"] = (
    (1 + df["Strategy_Return"]).cumprod()
)

# 7. Calculate performance metrics

total_return = (
    df["Cumulative_Strategy_Return"].iloc[-1] - 1
) * 100

active_trades = df[df["Position"].shift(1).fillna(0) != 0]

winning_trades = (
    active_trades["Strategy_Return"] > 0
).sum()

losing_trades = (
    active_trades["Strategy_Return"] < 0
).sum()

total_trades = len(active_trades)

win_rate = (
    winning_trades / total_trades * 100
    if total_trades > 0 else 0
)

print("\n========== BACKTEST PERFORMANCE ==========")

print("Total active sessions:", total_trades)
print("Winning sessions:", winning_trades)
print("Losing sessions:", losing_trades)
print("Win rate:", round(win_rate, 2), "%")
print("Total strategy return:", round(total_return, 2), "%")



# 8. Calculate NIFTY 50 buy-and-hold benchmark

df["Benchmark_Return"] = df["Close"].pct_change().fillna(0)

df["Cumulative_Benchmark"] = (
    (1 + df["Benchmark_Return"]).cumprod()
)

benchmark_return = (
    df["Cumulative_Benchmark"].iloc[-1] - 1
) * 100

print("\nNIFTY 50 buy-and-hold return:",
      round(benchmark_return, 2), "%")


# 9. Calculate maximum drawdown

df["Running_Peak"] = (
    df["Cumulative_Strategy_Return"].cummax()
)

df["Drawdown"] = (
    df["Cumulative_Strategy_Return"] /
    df["Running_Peak"] - 1
)

max_drawdown = df["Drawdown"].min() * 100


print("\n========== RISK AND BENCHMARK ANALYSIS ==========")

print("NIFTY 50 benchmark return:",
      round(benchmark_return, 2), "%")

print("Strategy maximum drawdown:",
      round(max_drawdown, 2), "%")



# 10. Save backtesting results

df.to_csv(OUTPUT_FILE, index_label="Date")

print("\nBacktesting results saved successfully!")
print("Saved file:", OUTPUT_FILE) 

