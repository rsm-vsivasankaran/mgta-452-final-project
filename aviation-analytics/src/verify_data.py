
import glob
import pandas as pd
from pathlib import Path

RAW_DIR = Path("aviation-analytics/data/raw/pireps")
all_files = glob.glob(str(RAW_DIR / "*.csv"))

print(f"Found {len(all_files)} files.")
if all_files:
    # Read first file to check columns
    first_file = all_files[0]
    print(f"Reading {first_file}...")
    df = pd.read_csv(first_file)
    print("Columns:", df.columns.tolist())
    print("First 5 rows:")
    print(df.head())
    
    # Check for specific columns expected
    for col in ['turbulence_intensity', 'latitude', 'longitude', 'timestamp', 'date_time', 'altitude_ft_msl']:
        if col in df.columns:
            print(f"Found expected column: {col}")
        else:
            # Check for case sensitivity or close matches
            matches = [c for c in df.columns if col in c.lower()]
            if matches:
                print(f"Found similar column for '{col}': {matches}")
            else:
                print(f"MISSING expected column: {col}")
else:
    print("No CSV files found in directory.")
