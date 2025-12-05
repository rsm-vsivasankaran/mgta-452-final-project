
import streamlit as st
import sys
import os

# Add src to path
sys.path.append(os.path.abspath("aviation-analytics/src"))
from ui_utils import apply_theme, render_header

# Page Config
st.set_page_config(
    page_title="MGTA-452 Final Project",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()
from ui_utils import render_sidebar, render_header
render_sidebar()

# Landing Page Content
render_header("Home <span style='padding-left: 10px; padding-right: 10px;'>|</span> Vigneshwaran Siva Sankaran <span style='padding-left: 5px; padding-right: 5px;'> • </span> Jing Luo <span style='padding-left: 5px; padding-right: 5px;'> • </span> Vivian Yang", "fa-solid fa-house")

st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <p style="font-size: 1.5rem; color: #8b949e;">Next-Gen Intelligence for Safer Skies & Efficient Operations</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: #161b22; padding: 30px; border-radius: 15px; border: 1px solid #30363d; height: 100%;">
        <h2 style="color: #7ee787;">🌪️ Turbulence Analytics</h2>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            Analyze global turbulence patterns using millions of Pilot Reports (PIREPs).
            Identify hotspots, visualize altitude risks, and predict severity in real-time.
        </p>
        <ul style="color: #8b949e; margin-top: 20px;">
            <li>3D Geospatial Visualization</li>
            <li>Real-time Risk Prediction Model</li>
            <li>Altitude & Seasonal Analysis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: #161b22; padding: 30px; border-radius: 15px; border: 1px solid #30363d; height: 100%;">
        <h2 style="color: #a5d6ff;">🛫 Airport Efficiency</h2>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            Evaluate operational performance of major airports. 
            Track delays, cancellations, and predict future bottlenecks using advanced regression models.
        </p>
        <ul style="color: #8b949e; margin-top: 20px;">
            <li>Efficiency Rankings & Scorecards</li>
            <li>Delay Prediction Engine</li>
            <li>Volume vs. Performance Correlation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.info("👈 **Select a module from the sidebar to begin your analysis.**")
