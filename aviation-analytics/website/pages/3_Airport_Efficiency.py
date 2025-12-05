
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys
import os

# Add src to path
sys.path.append(os.path.abspath("aviation-analytics/src"))
from ui_utils import apply_theme, render_header, render_metric_card, render_sidebar

st.set_page_config(page_title="Airport Efficiency", page_icon="🛫", layout="wide")
apply_theme()
render_sidebar()
render_header("Airport Efficiency Index (AEI)", "fa-solid fa-plane-departure")

PROCESSED_DIR = Path("aviation-analytics/data/processed")

@st.cache_data
def load_aei_data():
    path = PROCESSED_DIR / "airport_efficiency.csv.gz"
    if path.exists():
        return pd.read_csv(path, compression='gzip')
    return pd.DataFrame()

df = load_aei_data()

if not df.empty:
    # Top Level Metrics
    c1, c2, c3 = st.columns(3)
    # Color logic for metrics
    avg_delay = df['avg_dep_delay'].mean()
    delay_color = "#21c354" if avg_delay < 15 else "#ff4b4b"
    
    with c1: render_metric_card("Airports Tracked", f"{len(df)}")
    with c2: render_metric_card("Global Avg Delay", f"{avg_delay:.1f} min", color=delay_color)
    with c3: render_metric_card("Avg Cancel Rate", f"{df['cancellation_rate'].mean()*100:.2f}%")
    
    st.markdown("### 🏆 Efficiency Rankings")
    
    col1, col2 = st.columns(2)
    
    # Custom Gradient for Tables
    # Green for low delay, Red for high delay
    
    with col1:
        st.subheader("Top 10 Most Efficient")
        top_efficient = df.sort_values('avg_dep_delay').head(10)[['ORIGIN', 'avg_dep_delay', 'cancellation_rate']]
        st.dataframe(
            top_efficient.style
            .bar(subset=['avg_dep_delay'], color='#21c354')
            .format({'avg_dep_delay': "{:.1f}", 'cancellation_rate': "{:.2%}"}),
            use_container_width=True,
            hide_index=True
        )
        
    with col2:
        st.subheader("Top 10 Least Efficient")
        bottom_efficient = df.sort_values('avg_dep_delay', ascending=False).head(10)[['ORIGIN', 'avg_dep_delay', 'cancellation_rate']]
        st.dataframe(
            bottom_efficient.style
            .bar(subset=['avg_dep_delay'], color='#ff4b4b')
            .format({'avg_dep_delay': "{:.1f}", 'cancellation_rate': "{:.2%}"}),
            use_container_width=True,
            hide_index=True
        )
        
    st.markdown("### 📊 Advanced Analytics")
    
    # Compare Airports (Radar Chart)
    st.subheader("Airport Comparison (Radar Chart)")
    all_airports = sorted(df['ORIGIN'].unique())
    selected_airports = st.multiselect("Select Airports to Compare", all_airports, default=all_airports[:3])
    
    if selected_airports:
        compare_df = df[df['ORIGIN'].isin(selected_airports)].copy()
        
        # Normalize for Radar Chart
        import plotly.graph_objects as go
        from sklearn.preprocessing import MinMaxScaler
        
        scaler = MinMaxScaler()
        # Invert delay/cancel so higher is better for "Score"
        compare_df['Efficiency Score'] = 1 - scaler.fit_transform(compare_df[['avg_dep_delay']])
        compare_df['Reliability Score'] = 1 - scaler.fit_transform(compare_df[['cancellation_rate']])
        compare_df['Volume Score'] = scaler.fit_transform(compare_df[['total_flights']])
        
        categories = ['Efficiency Score', 'Reliability Score', 'Volume Score']
        
        fig_radar = go.Figure()
        
        for i, row in compare_df.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row['Efficiency Score'], row['Reliability Score'], row['Volume Score']],
                theta=categories,
                fill='toself',
                name=row['ORIGIN']
            ))
            
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1])
            ),
            showlegend=True,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            title="Performance Profile (Normalized)"
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Metric Correlations")
        # Correlation Heatmap
        corr = df[['total_flights', 'avg_dep_delay', 'cancellation_rate']].corr()
        fig_corr = px.imshow(corr, text_auto=True, aspect="auto",
                             color_continuous_scale='RdBu_r', title="KPI Correlation Heatmap",
                             template="plotly_dark")
        fig_corr.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_corr, use_container_width=True)
        
    with c2:
        st.subheader("Global Volume vs. Performance")
        fig = px.scatter(
            df, 
            x='total_flights', 
            y='avg_dep_delay', 
            hover_name='ORIGIN', 
            size='total_flights',
            color='avg_dep_delay',
            color_continuous_scale='RdYlGn_r', # Green to Red (Reversed)
            template="plotly_dark",
            title="Impact of Flight Volume on Delays"
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

else:
    st.error("AEI Data not found. Please run the data pipeline.")
