"""
Feature Generator

Reads all stock CSV files from:
data/raw/2026-07-01/

Calculates:
- SMA
- EMA
- RSI
- MACD
- Bollinger Bands
- ATR
- ADX

Saves the processed files to:
data/processed/YYYY-MM-DD/
"""

from pathlib import Path
from datetime import datetime

import pandas as pd

from INDICATORS.sma import add_sma
from INDICATORS.ema import add_ema
from INDICATORS.rsi import add_rsi
from INDICATORS.macd import add_macd
from INDICATORS.bollinger import add_bollinger
from INDICATORS.atr import add_atr
from INDICATORS.adx import add_adx

# -------------------------------------------------
# Project Paths
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "2026-07-01"

TODAY = datetime.now().strftime("%Y-%m-%d")

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / TODAY

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# -------------------------------------------------
# Read all CSV files
# -------------------------------------------------

csv_files = list(RAW_DATA_DIR.glob("*.csv"))

print(f"\nFound {len(csv_files)} stock files.\n")

# -------------------------------------------------
# Process every file
# -------------------------------------------------

for file in csv_files:

    print("=" * 60)
    print(f"Processing {file.name}")

    df = pd.read_csv(file)

    # Convert date column
    df["date"] = pd.to_datetime(df["date"])

    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)

    # -------------------------------------------------
    # Technical Indicators
    # -------------------------------------------------

    df = add_sma(df)
    df = add_ema(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_bollinger(df)
    df = add_atr(df)
    df = add_adx(df)

    # -------------------------------------------------
    # Save Processed File
    # -------------------------------------------------

    output_file = OUTPUT_DIR / file.name

    df.to_csv(
        output_file,
        index=False
    )

    print(f"Saved -> {output_file}")

print("\n========================================")
print("Feature Engineering Completed Successfully")
print(f"Processed Files : {len(csv_files)}")
print(f"Output Folder   : {OUTPUT_DIR}")
print("========================================")