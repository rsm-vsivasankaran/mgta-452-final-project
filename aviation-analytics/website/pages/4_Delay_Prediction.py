
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import sys
import os

# Add src to path
sys.path.append(os.path.abspath("aviation-analytics/src"))
from ui_utils import apply_theme, render_header, render_metric_card, render_sidebar

st.set_page_config(page_title="Delay Prediction", page_icon="⏱️", layout="wide")
apply_theme()
render_sidebar()
render_header("Flight Delay Prediction", "fa-solid fa-clock")

MODELS_DIR = Path("aviation-analytics/models")

@st.cache_resource
def load_aei_model():
    model_path = MODELS_DIR / "aei_model.pkl"
    if model_path.exists():
        return joblib.load(model_path)
    return None

model = load_aei_model()

# Initialize Session State
if 'delay_pred' not in st.session_state:
    st.session_state.delay_pred = None

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Operational Parameters")
    with st.form("aei_form"):
        vol = st.number_input("Projected Monthly Flights", value=5000, step=100)
        # avg_cancel = st.slider("Expected Cancellation Rate", 0.0, 0.1, 0.015, format="%.3f")
        # Hardcoding cancel rate for now as per model training simplification
        avg_cancel = 0.015
        
        submitted = st.form_submit_button("Predict Delay")
        
        if submitted and model:
            input_data = pd.DataFrame([[vol, avg_cancel]], 
                                      columns=['total_flights', 'cancellation_rate'])
            pred = model.predict(input_data)[0]
            
            # Sensitivity Analysis
            import numpy as np
            vol_range = np.linspace(vol * 0.5, vol * 1.5, 20)
            sensitivity_data = pd.DataFrame({
                'total_flights': vol_range,
                'cancellation_rate': avg_cancel
            })
            sensitivity_preds = model.predict(sensitivity_data)
            
            st.session_state.delay_pred = {
                "value": pred,
                "sensitivity": pd.DataFrame({'Volume': vol_range, 'Predicted Delay': sensitivity_preds})
            }

with col2:
    st.markdown("### Forecast")
    if st.session_state.delay_pred is not None:
        pred_val = st.session_state.delay_pred["value"]
        sens_df = st.session_state.delay_pred["sensitivity"]
        
        # Color coding
        if pred_val < 15: color = "#21c354" # Green
        elif pred_val < 30: color = "#ffa421" # Orange
        else: color = "#ff4b4b" # Red
        
        st.markdown(f"""
            <div style="
                background-color: #161b22; 
                border: 2px solid {color}; 
                border-radius: 15px; 
                padding: 30px; 
                text-align: center;
                margin-bottom: 20px;
                box-shadow: 0 0 20px {color}40;
            ">
                <h2 style="color: #8b949e; margin-bottom: 5px; font-size: 1rem;">ESTIMATED DELAY</h2>
                <h1 style="font-size: 3.5rem; color: {color}; margin: 0; font-weight: 800;">{pred_val:.1f} <span style="font-size: 1.5rem;">min</span></h1>
                <p style="color: #8b949e; margin-top: 10px; font-size: 0.9rem;">Volume: {vol:,} flights</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Volume Sensitivity Analysis")
        import plotly.express as px
        fig = px.area(sens_df, x='Volume', y='Predicted Delay', 
                      title="Projected Delay vs. Flight Volume",
                      template="plotly_dark")
        # Add vertical line for current volume
        fig.add_vline(x=vol, line_dash="dash", line_color="white", annotation_text="Current Volume")
        fig.update_traces(line_color=color)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        
    elif not model:
        st.warning("Model not found. Please train the model first.")
    else:
        st.info("Enter operational parameters and click Predict.")
