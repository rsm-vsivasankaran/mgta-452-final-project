
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import sys
import os
import numpy as np
import plotly.express as px

# Add src to path
sys.path.append(os.path.abspath("aviation-analytics/src"))
from ui_utils import apply_theme, render_header, render_metric_card, render_sidebar

st.set_page_config(page_title="Turbulence Prediction", page_icon="🔮", layout="wide")
apply_theme()
render_sidebar()
render_header("Turbulence Risk Prediction", "fa-solid fa-wind")

MODELS_DIR = Path("aviation-analytics/models")

@st.cache_resource
def load_model():
    model_path = MODELS_DIR / "turbulence_model.pkl"
    le_path = MODELS_DIR / "turbulence_le.pkl"
    if model_path.exists() and le_path.exists():
        return joblib.load(model_path), joblib.load(le_path)
    return None, None

model, le = load_model()

# Initialize Session State
if 'turb_pred' not in st.session_state:
    st.session_state.turb_pred = None

# Layout: Row 1 (Input | Result)
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Flight Parameters")
    with st.form("prediction_form"):
        c1, c2, c3 = st.columns(3)
        alt = c1.number_input("Altitude (ft)", value=30000, step=1000)
        lat = c2.number_input("Latitude", value=34.0)
        lon = c3.number_input("Longitude", value=-118.0)
        
        c4, c5 = st.columns(2)
        month = c4.slider("Month", 1, 12, 1)
        hour = c5.slider("Hour (UTC)", 0, 23, 12)
        
        submitted = st.form_submit_button("Predict Risk", use_container_width=True)
        
        if submitted and model:
            input_data = pd.DataFrame([[alt, lat, lon, month, hour]], 
                                      columns=['altitude', 'latitude', 'longitude', 'month', 'hour'])
            pred_encoded = model.predict(input_data)[0]
            pred_label = le.inverse_transform([pred_encoded])[0]
            pred_proba = model.predict_proba(input_data)[0]
            
            st.session_state.turb_pred = {
                "label": pred_label,
                "proba": dict(zip(le.classes_, pred_proba)),
                "inputs": {"alt": alt, "lat": lat, "lon": lon, "month": month, "hour": hour}
            }

with col2:
    st.markdown("### Risk Assessment")
    if st.session_state.turb_pred:
        result = st.session_state.turb_pred["label"]
        proba = st.session_state.turb_pred["proba"]
        
        # Gauge Chart
        import plotly.graph_objects as go
        
        # Map severity to 0-100 scale for gauge
        severity_score = 0
        if result == "Severe": severity_score = 90
        elif result == "Moderate": severity_score = 60
        elif result == "Light": severity_score = 30
        else: severity_score = 10
        
        color = "#21c354"
        if result == "Severe": color = "#ff4b4b"
        elif result == "Moderate": color = "#ffa421"
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = severity_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Turbulence Risk", 'font': {'size': 24, 'color': "#8b949e"}},
            delta = {'reference': 50, 'increasing': {'color': "#ff4b4b"}, 'decreasing': {'color': "#21c354"}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': color},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "#333",
                'steps': [
                    {'range': [0, 33], 'color': 'rgba(33, 195, 84, 0.3)'},
                    {'range': [33, 66], 'color': 'rgba(255, 164, 33, 0.3)'},
                    {'range': [66, 100], 'color': 'rgba(255, 75, 75, 0.3)'}],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': severity_score}}))
        
        fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white", 'family': "Arial"})
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.markdown(f"<h2 style='text-align: center; color: {color}; margin-top: -20px;'>{result.upper()}</h2>", unsafe_allow_html=True)
    elif not model:
        st.warning("Model not found. Please train the model first.")
    else:
        st.info("Enter flight parameters and click Predict.")

# Row 2: Charts (Side by Side)
if st.session_state.turb_pred:
    st.markdown("---")
    c_chart1, c_chart2 = st.columns(2)
    
    proba = st.session_state.turb_pred["proba"]
    color_map = {"Severe": "#ff4b4b", "Moderate": "#ffa421", "Light": "#21c354", "None": "#21c354"}
    
    with c_chart1:
        st.subheader("Prediction Confidence")
        
        # 1. Calculate Statistics
        severity_map = {"None": 0, "Light": 33, "Moderate": 66, "Severe": 100}
        probs = [proba.get(k, 0.0) for k in severity_map.keys()]
        values = list(severity_map.values())
        
        mean_severity = sum(p * v for p, v in zip(probs, values))
        variance = sum(p * ((v - mean_severity) ** 2) for p, v in zip(probs, values))
        std_dev = max(variance ** 0.5, 10)
        
        # 2. Generate Curve
        x = np.linspace(-10, 110, 500)
        y = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean_severity) / std_dev) ** 2)
        y_norm = y / y.max()
        
        # CI Bounds (95%)
        ci_lower = max(0, mean_severity - 1.96 * std_dev)
        ci_upper = min(100, mean_severity + 1.96 * std_dev)
        
        # 3. Plot
        fig_bell = go.Figure()
        
        # Severity Zones (Background)
        shapes = [
            dict(type="rect", x0=0, x1=33, y0=0, y1=1, xref="x", yref="paper", fillcolor="rgba(33, 195, 84, 0.1)", line_width=0, layer="below"),
            dict(type="rect", x0=33, x1=66, y0=0, y1=1, xref="x", yref="paper", fillcolor="rgba(255, 164, 33, 0.1)", line_width=0, layer="below"),
            dict(type="rect", x0=66, x1=100, y0=0, y1=1, xref="x", yref="paper", fillcolor="rgba(255, 75, 75, 0.1)", line_width=0, layer="below")
        ]
        
        # Full Distribution Curve
        fig_bell.add_trace(go.Scatter(
            x=x, y=y_norm, 
            mode='lines', 
            name='Probability Density',
            line=dict(color='#e0e0e0', width=2)
        ))
        
        # 95% Confidence Interval (Shaded Area)
        x_fill = np.linspace(ci_lower, ci_upper, 100)
        y_fill = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_fill - mean_severity) / std_dev) ** 2)
        y_fill = y_fill / y.max() # Normalize to match main curve
        
        fig_bell.add_trace(go.Scatter(
            x=x_fill, y=y_fill, 
            mode='lines', 
            fill='tozeroy',
            name='95% Confidence',
            line=dict(width=0),
            fillcolor='rgba(88, 166, 255, 0.4)'
        ))
        
        # Expected Severity Line
        fig_bell.add_vline(x=mean_severity, line_width=2, line_dash="dash", line_color="white", annotation_text="Exp. Value")
        
        fig_bell.update_layout(
            xaxis=dict(
                title="Severity Score", 
                range=[0, 100], 
                tickmode='array',
                tickvals=[16.5, 49.5, 83],
                ticktext=['Light', 'Moderate', 'Severe'],
                showgrid=False
            ),
            yaxis=dict(showticklabels=False, showgrid=False),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=30, b=0, l=0, r=0),
            height=300,
            shapes=shapes
        )
        st.plotly_chart(fig_bell, use_container_width=True)
        
    with c_chart2:
        st.subheader("Model Explanation")
        if hasattr(model, 'feature_importances_'):
            features = ['altitude', 'latitude', 'longitude', 'month', 'hour']
            importances = model.feature_importances_
            feat_df = pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values('Importance', ascending=True)
            
            fig_feat = px.bar(feat_df, x='Importance', y='Feature', orientation='h',
                              template="plotly_dark", color='Importance', color_continuous_scale='Blues')
            fig_feat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
            st.plotly_chart(fig_feat, use_container_width=True)
        else:
            st.info("Feature importance not available.")

    # Row 3: Forecast
    st.subheader("Forecast (Next 12 Hours)")
    
    # Retrieve inputs from session state
    inputs = st.session_state.turb_pred["inputs"]
    alt, lat, lon, month, hour = inputs['alt'], inputs['lat'], inputs['lon'], inputs['month'], inputs['hour']
    
    future_hours = [(hour + i) % 24 for i in range(12)]
    future_data = []
    
    for h in future_hours:
        row = pd.DataFrame([[alt, lat, lon, month, h]], 
                           columns=['altitude', 'latitude', 'longitude', 'month', 'hour'])
        p_proba = model.predict_proba(row)[0]
        classes = list(le.classes_)
        sev_idx = classes.index('Severe') if 'Severe' in classes else -1
        mod_idx = classes.index('Moderate') if 'Moderate' in classes else -1
        
        risk_score = 0
        if sev_idx != -1: risk_score += p_proba[sev_idx] * 1.0
        if mod_idx != -1: risk_score += p_proba[mod_idx] * 0.5
        
        future_data.append({'Hour (UTC)': h, 'Risk Score': risk_score})
        
    forecast_df = pd.DataFrame(future_data)
    
    fig_forecast = px.line(forecast_df, x='Hour (UTC)', y='Risk Score', markers=True,
                           title="Projected Turbulence Risk", template="plotly_dark")
    fig_forecast.update_traces(line_color='#ff4b4b', line_width=3)
    fig_forecast.add_hrect(y0=0.5, y1=1.0, line_width=0, fillcolor="red", opacity=0.2, annotation_text="High Risk")
    fig_forecast.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_forecast, use_container_width=True)
