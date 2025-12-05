
import streamlit as st

def apply_theme():
    """
    Injects custom CSS for the 'Dark Aviation' theme.
    """
    st.markdown("""
        <style>
        /* Main Background */
        .stApp {
            background-color: #0e1117;
            color: #e0e0e0;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #161b22;
            border-right: 1px solid #30363d;
        }
        
        /* Headers */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            color: #58a6ff; /* Aviation Blue */
        }
        
        /* Metric Cards */
        div.css-1r6slb0.e1tzin5v2 {
            background-color: #1f2428;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        
        /* Buttons */
        .stButton>button {
            background-color: #238636;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #2ea043;
        }
        
        /* Sidebar Navigation */
        .st-emotion-cache-16txtl3 { /* Target sidebar nav items */
            font-size: 1.2rem !important;
        }
        [data-testid="stSidebarNav"] span {
            font-size: 1.2rem !important;
            font-weight: 500;
        }
        
        /* Tables */
        .dataframe {
            font-family: 'Roboto Mono', monospace;
        }
        
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """, unsafe_allow_html=True)

def render_sidebar():
    """
    Renders the sidebar with project info and team members.
    """
    # with st.sidebar:
        # Spacer to push content to bottom
        # st.markdown("<div style='height: fill-available;'></div>", unsafe_allow_html=True)
        
        # st.markdown("""
        # <div style="color: #8b949e; font-size: 0.9rem; position: fixed; bottom: 0;">
        #     <h2 style="color: #7ee787;">👥 Team Members</h2>
        #     <ul style="list-style-type: none; padding: 0; margin: 0;">
        #         <li style="margin-bottom: 8px;">• Vigneshwaran Siva Sankaran</li>
        #         <li style="margin-bottom: 8px;">• Jing Luo</li>
        #         <li style="margin-bottom: 8px;">• Vivian Yang</li>
        #     </ul>
        # </div>
        # """, unsafe_allow_html=True)

def render_header(subtitle, icon_class="fa-solid fa-plane"):
    """
    Renders the standard header with 'Aviation Analytics' as the main title.
    Args:
        subtitle (str): The specific page title (e.g., 'Global Turbulence').
        icon_class (str): The FontAwesome icon class to display.
    """
    st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="font-size: 2.5rem; margin-right: 20px; color: #58a6ff;">
                <i class="{icon_class}"></i>
            </div>
            <div>
                <h1 style="margin: 0; color: #58a6ff; font-size: 2.5rem;">Aviation Analytics</h1>
                <p style="margin: 0; color: #8b949e; font-size: 1.2rem; font-weight: 500;">{subtitle}</p>
            </div>
        </div>
        <hr style="border-color: #30363d; margin-top: 0;">
    """, unsafe_allow_html=True)

def render_metric_card(label, value, delta=None, color="blue"):
    delta_html = ""
    if delta:
        delta_color = "#3fb950" if "+" in str(delta) or float(delta.strip('%')) > 0 else "#f85149"
        delta_html = f'<span style="color: {delta_color}; font-size: 0.9rem; margin-left: 10px;">{delta}</span>'
        
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1f2428 0%, #161b22 100%);
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
        ">
            <div style="color: #8b949e; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
            <div style="font-size: 2rem; font-weight: bold; color: #e0e0e0; margin-top: 5px;">
                {value} {delta_html}
            </div>
        </div>
    """, unsafe_allow_html=True)
