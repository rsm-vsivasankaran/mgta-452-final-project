
import glob
import pandas as pd
from pathlib import Path

RAW_DIR = Path("aviation-analytics/data/raw/pireps")
all_files = glob.glob(str(RAW_DIR / "*.csv"))

if all_files:
    # Read first file
    df = pd.read_csv(all_files[0])
    
    print("Unique TURBULENCE values:")
    print(df['TURBULENCE'].unique())
    
    print("\nUnique ICING values:")
    print(df['ICING'].unique())
    
    print("\nSample FL (Altitude) values:")
    print(df['FL'].head(10).tolist())
    
    print("\nSample VALID values:")
    print(df['VALID'].head(5).tolist())
