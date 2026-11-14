
"""
Project: NIFTY 50 Historical Data Analysis
Purpose: Download historical NIFTY 50 index data
"""

import yfinance as yf
import pandas as pd
from pathlib import Path

# 1. Define project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 2. Define output directory
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 3. NIFTY 50 Yahoo Finance ticker
TICKER = "^NSEI"

# 4. Download historical data
print("Downloading NIFTY 50 historical data...")

data = yf.download(
    TICKER,
    start="2015-01-01",
    end="2026-11-12",
    interval="1d",
    auto_adjust=True,
    progress=False
)

# 5. Check whether data was downloaded
if data.empty:
    print("ERROR: No data downloaded. Check your internet connection.")
else:
    # 6. Save data as CSV
    output_file = OUTPUT_DIR / "nifty50_historical.csv"
    data.to_csv(output_file)

    print("\nDownload successful!")
    print(f"Total records: {len(data)}")
    print(f"Saved at: {output_file}")

    # 7. Display first five records
    print("\nFirst five records:")
    print(data.head())

    print("\nData shape:", data.shape)
