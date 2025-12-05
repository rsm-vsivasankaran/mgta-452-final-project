
import os
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Add src to path
sys.path.append(os.path.abspath("aviation-analytics/src"))

from data_preprocessing import process_turbulence_data, process_aei_chunks

# Define Paths
RAW_DIR = Path("aviation-analytics/data/raw")
PROCESSED_DIR = Path("aviation-analytics/data/processed")
PIREPS_DIR = RAW_DIR / "pireps"

# Create directories if not exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# 1. Turbulence
print("Processing Turbulence Data...")
turbulence_df = process_turbulence_data(PIREPS_DIR)

if not turbulence_df.empty:
    print(f"Processed {len(turbulence_df)} rows.")
    output_path = PROCESSED_DIR / "turbulence_cleaned.csv.gz"
    turbulence_df.to_csv(output_path, compression='gzip', index=False)
    print(f"Saved to {output_path}")
else:
    print("No valid turbulence data found.")

# 2. AEI
print("\nStarting AEI Processing (Chunked Download)...")
YEARS = [2023, 2024]
MONTHS = range(1, 13)

aei_df = process_aei_chunks(YEARS, MONTHS)

if not aei_df.empty:
    print(f"Processed AEI for {len(aei_df)} airports.")
    print(aei_df.head())
    
    output_path = PROCESSED_DIR / "airport_efficiency.csv.gz"
    aei_df.to_csv(output_path, compression='gzip', index=False)
    print(f"Saved AEI data to {output_path}")
else:
    print("Failed to process AEI data.")
