
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

file_path = PROJECT_ROOT / "data" / "raw" / "nifty50_historical.csv"

df = pd.read_csv(file_path, header=[0, 1], index_col=0)

print("DATASET VERIFICATION")
print("--------------------")

print("Shape:", df.shape)
print("\nColumns:")
print(df.columns)

print("\nFirst 5 records:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print("\nDate range:")
print(df.index.min(), "to", df.index.max())
