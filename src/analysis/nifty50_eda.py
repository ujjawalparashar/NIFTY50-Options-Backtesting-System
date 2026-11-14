
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "nifty50_clean.csv"
OUTPUT_DIR = PROJECT_ROOT / "reports" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load cleaned dataset
df = pd.read_csv(INPUT_FILE, index_col=0, parse_dates=True)

# Calculate daily returns
df["Daily_Return"] = df["Close"].pct_change() * 100

# Calculate moving averages
df["MA_20"] = df["Close"].rolling(window=20).mean()
df["MA_50"] = df["Close"].rolling(window=50).mean()

# Calculate volatility
daily_volatility = df["Daily_Return"].std()
annual_volatility = daily_volatility * np.sqrt(252)

# Calculate maximum drawdown
df["Peak"] = df["Close"].cummax()
df["Drawdown"] = (
    (df["Close"] - df["Peak"]) / df["Peak"]
) * 100

max_drawdown = df["Drawdown"].min()

# Display statistics
print("NIFTY 50 EXPLORATORY DATA ANALYSIS")
print("---------------------------------")

print("Total trading sessions:", len(df))
print("Highest closing price:", df["Close"].max())
print("Lowest closing price:", df["Close"].min())
print("Average daily return:", df["Daily_Return"].mean())
print("Daily volatility:", daily_volatility)
print("Annualised volatility:", annual_volatility)
print("Maximum drawdown (%):", max_drawdown)

# Plot closing price and moving averages
plt.figure(figsize=(14, 7))

plt.plot(df.index, df["Close"], label="NIFTY 50 Close")
plt.plot(df.index, df["MA_20"], label="20-Day MA")
plt.plot(df.index, df["MA_50"], label="50-Day MA")

plt.title("NIFTY 50 Historical Price Analysis")
plt.xlabel("Date")
plt.ylabel("Index Value")
plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "nifty50_moving_averages.png",
    dpi=300
)

plt.show()

print("\nEDA completed successfully!")