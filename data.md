# 📄 Dataset List for Aviation Analytics Project

| Module | Dataset | Description | Format | Download Link |
|--------|---------|-------------|---------|----------------|
| **Turbulence** | **PIREP Turbulence Reports** | Pilot-reported turbulence (Light/Moderate/Severe) with lat/long/alt/time | CSV | https://mesonet.agron.iastate.edu/request/pireps/ |
| **Turbulence** | **ERA5 Atmospheric Reanalysis** | Global weather: wind, temp, humidity, pressure, shear (hourly) | NetCDF | https://cds.climate.copernicus.eu/cdsapp\#!/dataset/reanalysis-era5-single-levels |
| **Turbulence** | **ERA5 Pressure-Level Data** (optional but recommended) | Wind U/V components, temperature at multiple altitudes (pressure levels) | NetCDF | https://cds.climate.copernicus.eu/cdsapp\#!/dataset/reanalysis-era5-pressure-levels |
| **Turbulence** | **OpenSky Historical Trajectories** | Per-aircraft positions (lat/long/alt/time), great for route visualizations | CSV / Parquet | https://zenodo.org/communities/opensky-network/ |
| **AEI** | **BTS On-Time Performance** | US flight data: departure delay, arrival delay, taxi-in/out, cancellations | CSV | https://www.transtats.bts.gov/Tables.asp?DB_ID=120 |
| **AEI** | **BTS T-100 Traffic Data** | Traffic volume per airport: arrivals, departures, passengers | CSV | https://www.transtats.bts.gov/Tables.asp?DB_ID=111 |
| **AEI** | **ICAO Airport Database** (Open version) | Global airport locations, ICAO/IATA codes, metadata | CSV | https://ourairports.com/data/ |