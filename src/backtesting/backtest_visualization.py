"""
Project: NIFTY 50 Historical Data Analysis
Module: Backtesting Visualization
Purpose: Visualize strategy performance and risk.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# 1. Define project directories

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nifty50_backtest_results.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "reports"
    / "figures"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Project directory:", PROJECT_ROOT)
print("Input file:", INPUT_FILE)
print("Output directory:", OUTPUT_DIR)


# 2. Load backtesting results

df = pd.read_csv(INPUT_FILE, index_col=0, parse_dates=True)

print("\nBacktesting dataset loaded successfully!")
print("Total records:", len(df))

print("\nAvailable columns:")
print(df.columns.tolist())

print("\nLast 5 records:")
print(df.tail())


# 3. Plot cumulative strategy vs benchmark returns

strategy_returns = (
    df["Cumulative_Strategy_Return"] - 1
) * 100

benchmark_returns = (
    df["Cumulative_Benchmark"] - 1
) * 100

plt.figure(figsize=(14, 6))

plt.plot(
    df.index,
    strategy_returns,
    label="MA20 + MA50 + RSI Strategy"
)

plt.plot(
    df.index,
    benchmark_returns,
    label="NIFTY 50 Buy and Hold"
)

plt.title("Strategy Performance vs NIFTY 50")
plt.xlabel("Date")
plt.ylabel("Cumulative Return (%)")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "cumulative_returns.png",
    dpi=300
)

plt.show()

print("Cumulative returns graph saved successfully!")


# 4. Plot strategy drawdown

drawdown = df["Drawdown"] * 100

plt.figure(figsize=(14, 5))

plt.plot(
    df.index,
    drawdown,
    label="Strategy Drawdown"
)

plt.title("Strategy Drawdown Analysis")
plt.xlabel("Date")
plt.ylabel("Drawdown (%)")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "strategy_drawdown.png",
    dpi=300
)

plt.show()

print("Drawdown graph saved successfully!")


