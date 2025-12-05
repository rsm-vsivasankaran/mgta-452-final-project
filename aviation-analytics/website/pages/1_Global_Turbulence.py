
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
from pathlib import Path
import sys
import os

# Add src to path
sys.path.append(os.path.abspath("aviation-analytics/src"))
from ui_utils import apply_theme, render_header, render_metric_card, render_sidebar

st.set_page_config(page_title="Global Turbulence", page_icon="✈️", layout="wide")
apply_theme()
render_sidebar()
render_header("Global Turbulence Analytics", "fa-solid fa-earth-americas")

# Paths
PROCESSED_DIR = Path("aviation-analytics/data/processed")

@st.cache_data
def load_data():
    path = PROCESSED_DIR / "turbulence_cleaned.csv.gz"
    if path.exists():
        return pd.read_csv(path, compression='gzip') 
    return pd.DataFrame()

df = load_data()

if not df.empty:
    # Sidebar Filters
    st.sidebar.header("Filters")
    intensity_filter = st.sidebar.multiselect(
        "Turbulence Intensity",
        options=df['turbulence_intensity'].unique(),
        default=['Severe', 'Moderate']
    )
    
    min_alt, max_alt = int(df['altitude'].min()), int(df['altitude'].max())
    altitude_range = st.sidebar.slider("Altitude (ft)", min_alt, max_alt, (20000, 40000))
    
    # Filter Data
    filtered_df = df[
        (df['turbulence_intensity'].isin(intensity_filter)) &
        (df['altitude'].between(altitude_range[0], altitude_range[1]))
    ].copy()
    
    # Metrics
    c1, c2, c3 = st.columns(3)
    with c1: render_metric_card("Total Reports", f"{len(filtered_df):,}")
    with c2: render_metric_card("Severe Events", f"{len(filtered_df[filtered_df['turbulence_intensity']=='Severe']):,}")
    with c3: render_metric_card("Avg Altitude", f"{filtered_df['altitude'].mean():.0f} ft")
    
    # Plotly Density Mapbox
    st.subheader("Global Turbulence Heatmap")
    
    # Sampling for Performance (2D is lighter, can handle more, but keep safe)
    if len(filtered_df) > 20000:
        st.caption(f"⚠️ Displaying a random sample of 20,000 points (out of {len(filtered_df):,}) for performance.")
        map_df = filtered_df.sample(20000)
    else:
        map_df = filtered_df

    fig_map = px.density_mapbox(
        map_df, 
        lat='latitude', 
        lon='longitude', 
        z=None, # Just density of points
        radius=10,
        center=dict(lat=37, lon=-95), 
        zoom=3,
        mapbox_style="carto-darkmatter",
        title="Turbulence Density"
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Charts
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Altitude vs Intensity Risk")
        # Box Plot
        fig_box = px.box(filtered_df, x='turbulence_intensity', y='altitude', 
                         color='turbulence_intensity',
                         color_discrete_map={'Severe': '#ff4b4b', 'Moderate': '#ffa421', 'Light': '#21c354'},
                         template="plotly_dark",
                         title="Safe vs Risky Flight Levels")
        fig_box.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_box, use_container_width=True)
        
    with c2:
        st.subheader("Seasonal Trends")
        # Ensure timestamp is datetime
        filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'])
        monthly_counts = filtered_df.resample('ME', on='timestamp').size().reset_index(name='count')
        fig_trend = px.line(monthly_counts, x='timestamp', y='count', template="plotly_dark", markers=True,
                            title="Turbulence Events over Time")
        fig_trend.update_traces(line_color='#58a6ff')
        fig_trend.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")
    st.subheader("✈️ Route Turbulence Profile")
    
    # Hardcoded coordinates for major US airports
    AIRPORT_COORDS = {
        "JFK": {"lat": 40.6413, "lon": -73.7781},
        "LAX": {"lat": 33.9416, "lon": -118.4085},
        "ORD": {"lat": 41.9742, "lon": -87.9073},
        "DFW": {"lat": 32.8998, "lon": -97.0403},
        "DEN": {"lat": 39.8561, "lon": -104.6737},
        "SFO": {"lat": 37.6213, "lon": -122.3790},
        "SEA": {"lat": 47.4502, "lon": -122.3088},
        "MIA": {"lat": 25.7959, "lon": -80.2870},
        "ATL": {"lat": 33.6407, "lon": -84.4277},
        "BOS": {"lat": 42.3656, "lon": -71.0096}
    }
    
    rc1, rc2 = st.columns(2)
    origin = rc1.selectbox("Origin", list(AIRPORT_COORDS.keys()), index=0)
    dest = rc2.selectbox("Destination", list(AIRPORT_COORDS.keys()), index=1)
    
    if origin != dest:
        # Simple linear interpolation for route path
        start = AIRPORT_COORDS[origin]
        end = AIRPORT_COORDS[dest]
        
        # Filter data within a bounding box of the route + buffer
        lat_min, lat_max = min(start['lat'], end['lat']) - 2, max(start['lat'], end['lat']) + 2
        lon_min, lon_max = min(start['lon'], end['lon']) - 2, max(start['lon'], end['lon']) + 2
        
        route_df = filtered_df[
            (filtered_df['latitude'].between(lat_min, lat_max)) & 
            (filtered_df['longitude'].between(lon_min, lon_max))
        ]
        
        if not route_df.empty:
            # Visualize turbulence along the approximate path
            fig_route = px.scatter(route_df, x='longitude', y='latitude', color='turbulence_intensity',
                                   color_discrete_map={'Severe': '#ff4b4b', 'Moderate': '#ffa421', 'Light': '#21c354'},
                                   title=f"Turbulence Reports along {origin} -> {dest} Corridor",
                                   template="plotly_dark")
            
            # Add route line
            fig_route.add_shape(type="line",
                x0=start['lon'], y0=start['lat'], x1=end['lon'], y1=end['lat'],
                line=dict(color="white", width=2, dash="dash"),
            )
            fig_route.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_route, use_container_width=True)
        else:
            st.info("No turbulence reports found along this route corridor.")
    else:
        st.warning("Select different Origin and Destination.")

else:
    st.error("Data not found. Please run the data pipeline.")
