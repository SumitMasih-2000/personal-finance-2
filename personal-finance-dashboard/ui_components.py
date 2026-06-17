import streamlit as st

def set_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Finance Dashboard",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background-color: #f8fafc;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .main {
            background-color: #f8fafc;
            padding: 2rem;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: white;
            border-right: 1px solid #e5e7eb;
        }
        
        /* Headers */
        h1 {
            color: #1f2937;
            margin-bottom: 0.5rem;
            font-size: 2.5rem;
            font-weight: 700;
        }
        
        h2 {
            color: #374151;
            margin-top: 2rem;
            margin-bottom: 1rem;
            font-size: 1.5rem;
            font-weight: 600;
            border-bottom: 2px solid #2563eb;
            padding-bottom: 0.5rem;
        }
        
        h3 {
            color: #4b5563;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.8rem;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
        
        .stButton > button:hover {
            box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
            transform: translateY(-2px);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #f3f4f6;
            color: #6b7280;
            border-radius: 8px 8px 0 0;
            padding: 0.8rem 1.5rem;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #2563eb;
            color: white;
        }
        
        /* Selectbox and inputs */
        .stSelectbox, .stMultiSelect, .stDateInput {
            background-color: white;
            border-radius: 8px;
        }
        
        /* Cards container */
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #2563eb;
        }
        
        /* Text styling */
        .success-text { color: #10b981; font-weight: 600; }
        .danger-text { color: #ef4444; font-weight: 600; }
        .warning-text { color: #f59e0b; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

def get_metric_card_html(label, value, change=None, color="primary"):
    """Create HTML for metric card"""
    color_map = {
        "primary": "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);",
        "success": "background: linear-gradient(135deg, #10b981 0%, #059669 100%);",
        "warning": "background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);",
        "danger": "background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);" 
    }
    
    change_html = f"<div style='font-size: 0.85rem; opacity: 0.8; margin-top: 0.5rem;'>{change}</div>" if change else ""
    
    return f"""
    <div style="{color_map.get(color, color_map['primary'])}
                color: white;
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);">
        <h3 style='font-size: 0.9rem; font-weight: 600; text-transform: uppercase; 
                   letter-spacing: 0.5px; opacity: 0.9; margin: 0; margin-bottom: 0.5rem;'>{label}</h3>
        <div style='font-size: 1.8rem; font-weight: 700; margin: 0.5rem 0;'>{value}</div>
        {change_html}
    </div>
    """
