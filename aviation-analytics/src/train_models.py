
import pandas as pd
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath("aviation-analytics/src"))

from modeling import train_turbulence_model, train_aei_model

PROCESSED_DIR = Path("aviation-analytics/data/processed")

def main():
    # 1. Train Turbulence Model
    turb_path = PROCESSED_DIR / "turbulence_cleaned.csv.gz"
    if turb_path.exists():
        print(f"Loading Turbulence Data from {turb_path}...")
        # Read a sample if too large, or full
        # Using chunksize or nrows might be needed for 2M rows if memory is tight
        # But 2M rows with few columns is ~100MB, should be fine.
        df_turb = pd.read_csv(turb_path, compression='gzip')
        
        # Convert timestamp back to datetime
        df_turb['timestamp'] = pd.to_datetime(df_turb['timestamp'])
        
        train_turbulence_model(df_turb)
    else:
        print(f"Turbulence data not found at {turb_path}")

    # 2. Train AEI Model
    aei_path = PROCESSED_DIR / "airport_efficiency.csv.gz"
    if aei_path.exists():
        print(f"Loading AEI Data from {aei_path}...")
        df_aei = pd.read_csv(aei_path, compression='gzip')
        train_aei_model(df_aei)
    else:
        print(f"AEI data not found at {aei_path}")

if __name__ == "__main__":
    main()
