
import pandas as pd
from pathlib import Path

# Project directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Input and output paths
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "nifty50_historical.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "nifty50_clean.csv"

# Read original dataset
df = pd.read_csv(
    INPUT_FILE,
    header=[0, 1],
    index_col=0
)

# Flatten multi-level column names
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Prepare date column
df.index = pd.to_datetime(df.index)
df.index.name = "Date"

# Remove duplicate columns and rows
df = df.loc[:, ~df.columns.duplicated()]
df = df[~df.index.duplicated(keep="first")]

# Sort by date
df = df.sort_index()

# Convert values into numeric format
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows with missing values
df = df.dropna()

# Save cleaned dataset
df.to_csv(OUTPUT_FILE)

# Display results
print("DATA CLEANING COMPLETED")
print("-----------------------")

print("Total records:", len(df))
print("Columns:", list(df.columns))
print("Missing values:", df.isnull().sum().sum())

print("\nFirst five records:")
print(df.head())

print("\nCleaned file saved at:")
print(OUTPUT_FILE)
