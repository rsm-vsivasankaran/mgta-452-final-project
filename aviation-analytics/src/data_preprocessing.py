
import pandas as pd
import numpy as np
import glob
import requests
import zipfile
import io
from pathlib import Path

def standardize_turbulence(text):
    """
    Standardizes turbulence text labels into categories: 'Severe', 'Moderate', 'Light', 'None'.
    """
    if pd.isna(text):
        return None
    text = str(text).upper()
    
    if 'SEV' in text or 'EXTRM' in text:
        return 'Severe'
    if 'MOD' in text:
        return 'Moderate'
    if 'LGT' in text or 'LIGHT' in text:
        return 'Light'
    if 'NEG' in text or 'SMOOTH' in text or 'NONE' in text:
        return 'None'
    
    return None

def process_turbulence_data(raw_dir_path):
    """
    Loads and processes PIREPs CSV files from the specified directory.
    Returns a cleaned DataFrame.
    """
    raw_dir = Path(raw_dir_path)
    all_files = glob.glob(str(raw_dir / "*.csv"))
    print(f"Found {len(all_files)} files in {raw_dir}")
    
    df_list = []
    for filename in all_files:
        try:
            # Optimize: Reading chunks if needed, but lets try full
            df = pd.read_csv(filename, usecols=['VALID', 'LAT', 'LON', 'FL', 'TURBULENCE'])
            df_list.append(df)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            
    if not df_list:
        return pd.DataFrame()
        
    combined_df = pd.concat(df_list, ignore_index=True)
    
    combined_df = combined_df.rename(columns={
        'VALID': 'timestamp',
        'LAT': 'latitude',
        'LON': 'longitude',
        'FL': 'altitude',
        'TURBULENCE': 'raw_turbulence'
    })
    
    # Cleaning
    combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'], format='%Y%m%d%H%M', errors='coerce')
    combined_df['turbulence_intensity'] = combined_df['raw_turbulence'].apply(standardize_turbulence)
    
    combined_df['latitude'] = pd.to_numeric(combined_df['latitude'], errors='coerce')
    combined_df['longitude'] = pd.to_numeric(combined_df['longitude'], errors='coerce')
    combined_df['altitude'] = pd.to_numeric(combined_df['altitude'], errors='coerce')
    
    combined_df = combined_df.dropna(subset=['timestamp', 'latitude', 'longitude', 'turbulence_intensity'])
    
    combined_df = combined_df[
        (combined_df['latitude'] >= -90) & (combined_df['latitude'] <= 90) &
        (combined_df['longitude'] >= -180) & (combined_df['longitude'] <= 180)
    ]
    
    return combined_df

def download_aei_month(year: int, month: int) -> pd.DataFrame:
    """
    Downloads and returns a specific month of BTS On-Time Performance data.
    """
    url = (
        "https://transtats.bts.gov/"
        f"PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{year}_{month}.zip"
    )
    print(f"Downloading AEI data for {year}-{month}...")
    try:
        r = requests.get(url, verify=False) # Verify=False sometimes needed for BTS legacy certs, but try standard first if possible. 
        # Note: requests.get might fail with SSL error on some envs for BTS. 
        # If verify=False is needed, we'll add it. For now, assuming standard.
        # Actually, let's use verify=False to be safe as BTS certs are often tricky, 
        # but suppression of warnings is needed.
        
        r.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
            csv_name = [n for n in zf.namelist() if n.lower().endswith(".csv")][0]
            with zf.open(csv_name) as f:
                # Read only necessary columns to save memory
                # Columns: Year, Month, DayofMonth, FlightDate, Reporting_Airline, Origin, Dest, DepDelay, ArrDelay, Cancelled, Diverted
                cols = [
                    'Year', 'Month', 'DayofMonth', 'Reporting_Airline', 
                    'Origin', 'Dest', 'DepDelay', 'ArrDelay', 'Cancelled', 'Diverted'
                ]
                # BTS columns are often mixed case, but let's try to match standard names or read all then filter
                # To be safe, read header first? No, just read all and filter columns by name case-insensitive
                df = pd.read_csv(f, nrows=1)
                available_cols = df.columns.tolist()
                use_cols = [c for c in available_cols if c in cols or c.upper() in [x.upper() for x in cols]]
                
                f.seek(0)
                df = pd.read_csv(f, usecols=use_cols)
                
                # Standardize column names
                df.columns = [c.upper() for c in df.columns] # ORIGIN, DEST, DEPDELAY...
                
                # Map DEPDELAY to DEP_DELAY if needed (BTS usually has DepDelay or DEP_DELAY)
                # Let's check what we have
                rename_map = {}
                for c in df.columns:
                    if c == 'DEPDELAY': rename_map[c] = 'DEP_DELAY'
                    if c == 'ARRDELAY': rename_map[c] = 'ARR_DELAY'
                df = df.rename(columns=rename_map)
                
                return df
    except Exception as e:
        print(f"Failed to download/process {year}-{month}: {e}")
        return pd.DataFrame()

def process_aei_chunks(years, months):
    """
    Downloads and aggregates AEI data for specified years and months.
    Returns an aggregated DataFrame with efficiency metrics per airport.
    """
    aggregated_stats = []
    
    for year in years:
        for month in months:
            df = download_aei_month(year, month)
            if not df.empty:
                # Aggregate per month to save memory
                # We need: Origin, Count, Sum(DepDelay), Sum(Cancelled)
                
                # Ensure columns exist
                if 'DEP_DELAY' not in df.columns:
                    # Try to find it
                    print(f"DEP_DELAY missing in {year}-{month}. Cols: {df.columns}")
                    continue
                    
                # Fill NA delays with 0 for calculation (or drop?) 
                # Usually cancelled flights have NaN delay. 
                # We want to count cancellations separately.
                
                df['is_cancelled'] = df['CANCELLED'].fillna(0)
                df['dep_delay_clean'] = df['DEP_DELAY'].fillna(0)
                
                stats = df.groupby('ORIGIN').agg(
                    total_flights=('ORIGIN', 'count'),
                    total_dep_delay=('dep_delay_clean', 'sum'),
                    total_cancelled=('is_cancelled', 'sum')
                ).reset_index()
                
                stats['year'] = year
                stats['month'] = month
                aggregated_stats.append(stats)
    
    if not aggregated_stats:
        return pd.DataFrame()
        
    # Combine all monthly stats
    all_stats = pd.concat(aggregated_stats, ignore_index=True)
    
    # Final Aggregation per Airport
    final_efficiency = all_stats.groupby('ORIGIN').agg(
        total_flights=('total_flights', 'sum'),
        total_dep_delay=('total_dep_delay', 'sum'),
        total_cancelled=('total_cancelled', 'sum')
    ).reset_index()
    
    # Calculate Metrics
    final_efficiency['avg_dep_delay'] = final_efficiency['total_dep_delay'] / final_efficiency['total_flights']
    final_efficiency['cancellation_rate'] = final_efficiency['total_cancelled'] / final_efficiency['total_flights']
    
    # Filter for significant airports (e.g. > 1000 flights total in the period)
    final_efficiency = final_efficiency[final_efficiency['total_flights'] > 1000]
    
    return final_efficiency
