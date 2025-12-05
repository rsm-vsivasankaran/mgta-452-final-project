import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np
import os
import sys

# Add src to path
sys.path.append(os.path.abspath("aviation-analytics/src"))
from ui_utils import apply_theme, render_header, render_metric_card, render_sidebar

# Page Config
st.set_page_config(page_title="Airline Comparisons", page_icon="✈️", layout="wide")
apply_theme()
render_sidebar()

# Title
render_header("Airline & Airport Comparisons", "fa-solid fa-chart-bar")
st.markdown("### Deep Dive into Delay Drivers and Performance")

# Load Data
@st.cache_data
def load_data():
    # Adjust path to where the CSV is located relative to this file
    # Assuming website/pages/5_...py, and csv is in aviation-analytics/Airline_Delay_Cause.csv
    # We need to go up two levels: pages -> website -> aviation-analytics
    
    # Try absolute path based on known structure or relative
    possible_paths = [
        "../../Airline_Delay_Cause.csv",
        "Airline_Delay_Cause.csv",
        "/Users/dote/Documents/UCSD/MGTA452 - Large Data/Final Project/mgta-452-final-project/aviation-analytics/Airline_Delay_Cause.csv"
    ]
    
    df = None
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break
            
    if df is None:
        st.error("Could not find 'Airline_Delay_Cause.csv'. Please ensure the data file is present.")
        return None

    # Data Processing
    # 1. Calculate Delay Rate
    # Avoid division by zero
    df = df[df["arr_flights"] > 0].copy()
    df["delay_rate"] = df["arr_del15"] / df["arr_flights"]
    
    # 2. Create Timestamp
    df["timestamp"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"].astype(str))
    
    return df

df = load_data()

if df is not None:
    # --- Layout: Top Metrics ---
    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric_card("Total Flights Analyzed", f"{df['arr_flights'].sum():,.0f}")
    with col2:
        render_metric_card("Avg Delay Rate (Global)", f"{df['delay_rate'].mean():.2%}")
    with col3:
        render_metric_card("Total Delayed Flights", f"{df['arr_del15'].sum():,.0f}")

    st.markdown("---")

    # --- Section 1: Carrier & Airport Performance ---
    st.subheader("📊 Carrier & Airport Performance")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("**Average Delay Rate by Carrier**")
        carrier_delay = df.groupby("carrier")["delay_rate"].mean().sort_values(ascending=True).reset_index()
        fig_carrier = px.bar(
            carrier_delay, 
            x="delay_rate", 
            y="carrier", 
            orientation='h',
            color="delay_rate",
            color_continuous_scale="RdYlGn_r", # Red for high delay, Green for low
            labels={"delay_rate": "Delay Rate", "carrier": "Carrier"},
            height=500,
            template="plotly_dark"
        )
        fig_carrier.update_layout(xaxis_tickformat=".1%", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_carrier, use_container_width=True)
        
    with c2:
        st.markdown("**Top 20 Airports by Delay Rate**")
        # Filter for airports with significant traffic to avoid outliers from tiny airports
        # Let's take top 50 airports by volume first, then sort by delay rate
        top_airports_vol = df.groupby("airport")["arr_flights"].sum().nlargest(50).index
        airport_delay = df[df["airport"].isin(top_airports_vol)].groupby("airport")["delay_rate"].mean().sort_values(ascending=True).tail(20).reset_index()
        
        fig_airport = px.bar(
            airport_delay,
            x="delay_rate",
            y="airport",
            orientation='h',
            color="delay_rate",
            color_continuous_scale="Reds",
            labels={"delay_rate": "Delay Rate", "airport": "Airport"},
            height=500,
            template="plotly_dark"
        )
        fig_airport.update_layout(xaxis_tickformat=".1%", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_airport, use_container_width=True)

    st.markdown("---")

    # --- Section 2: Delay Causes & Trends ---
    st.subheader("📉 Causes & Trends")
    
    c3, c4 = st.columns(2)
    
    with c3:
        st.markdown("**Average Delay Minutes by Cause**")
        cause_cols = [
            "carrier_delay",
            "weather_delay",
            "nas_delay",
            "security_delay",
            "late_aircraft_delay",
        ]
        # Calculate mean for each cause
        cause_means = df[cause_cols].mean().reset_index()
        cause_means.columns = ["Cause", "Average Minutes"]
        cause_means = cause_means.sort_values(by="Average Minutes", ascending=True)
        
        fig_cause = px.bar(
            cause_means,
            x="Average Minutes",
            y="Cause",
            orientation='h',
            color="Average Minutes",
            color_continuous_scale="Blues",
            height=400,
            template="plotly_dark"
        )
        fig_cause.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_cause, use_container_width=True)
        
    with c4:
        st.markdown("**Monthly Delay Trend Over Time**")
        monthly_trend = df.groupby("timestamp")["delay_rate"].mean().reset_index()
        
        fig_trend = px.line(
            monthly_trend,
            x="timestamp",
            y="delay_rate",
            markers=True,
            labels={"delay_rate": "Average Delay Rate", "timestamp": "Date"},
            height=400,
            template="plotly_dark"
        )
        fig_trend.update_traces(line_color="#00CC96")
        fig_trend.update_layout(yaxis_tickformat=".1%", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")

    # --- Section 3: Advanced Analytics (Regression) ---
    st.subheader("🧠 Factor Importance Analysis")
    st.info("This analysis uses a Linear Regression model to determine which delay factors have the strongest relative influence on the overall Delay Rate.")

    # Prepare Data for Regression (Monthly Aggregation)
    # We aggregate by month to reduce noise and match the notebook's approach
    monthly_agg = df.groupby("timestamp")[cause_cols + ["delay_rate"]].mean().reset_index()
    
    X = monthly_agg[cause_cols]
    y = monthly_agg["delay_rate"]
    
    # Fit Model
    reg = LinearRegression()
    reg.fit(X, y)
    
    # Extract Coefficients
    coef_df = pd.DataFrame({"Factor": cause_cols, "Coefficient": reg.coef_})
    coef_df["Abs_Coefficient"] = coef_df["Coefficient"].abs()
    
    # Normalize for Radar Chart (0 to 1 scale)
    # This helps visualize relative importance
    min_val = coef_df["Abs_Coefficient"].min()
    max_val = coef_df["Abs_Coefficient"].max()
    coef_df["Normalized Importance"] = (coef_df["Abs_Coefficient"] - min_val) / (max_val - min_val)
    
    # Radar Chart
    categories = coef_df["Factor"].tolist()
    values = coef_df["Normalized Importance"].tolist()
    
    # Close the loop for radar chart
    categories = categories + [categories[0]]
    values = values + [values[0]]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Factor Importance',
        line_color='#AB63FA'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            ),
            bgcolor="#1f2428"
        ),
        showlegend=False,
        height=500,
        title="Relative Importance of Delay Factors (Normalized)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    
    c5, c6 = st.columns([2, 1])
    with c5:
        st.plotly_chart(fig_radar, use_container_width=True)
    with c6:
        st.markdown("#### Key Insights")
        st.write("The regression coefficients indicate the strength of the relationship between each delay cause and the overall delay rate.")
        
        # Display top factor
        top_factor = coef_df.sort_values("Abs_Coefficient", ascending=False).iloc[0]
        st.success(f"**{top_factor['Factor']}** has the highest influence on monthly delay rate variations.")
        
        st.dataframe(
            coef_df[["Factor", "Abs_Coefficient"]].sort_values("Abs_Coefficient", ascending=False).style.background_gradient(cmap="Purples"),
            use_container_width=True
        )

