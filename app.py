import streamlit as st
import pandas as pd
import numpy as np
from src.processor import get_detailed_profile, smart_cleaner
from src.charts import render_universal_chart
from groq import Groq
import time

# 1. ELITE UI CONFIGURATION (Ultra-Wide Glassmorphism)
st.set_page_config(
    page_title="Universal Visualizer Ultra",
    page_icon="🛡️",
    layout="wide",  # Solves congested layout
    initial_sidebar_state="expanded"
)

# Professional CSS for True Black and Spaced UI
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .block-container { padding: 2rem 3rem; }
    [data-testid="stMetricValue"] {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px 10px 0 0;
        padding: 0 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SECURE AI INITIALIZATION
def get_ai_client():
    if "GROQ_API_KEY" in st.secrets:
        return Groq(api_key=st.secrets["GROQ_API_KEY"])
    return None

client = get_ai_client()

# 3. MAIN APPLICATION ORCHESTRATOR
st.title("🛡️ Universal Visualizer Ultra")
st.caption("Professional-Grade Data Intelligence & Visualization Suite")

if "history" not in st.session_state:
    st.session_state.history = []

uploaded_file = st.file_uploader("Upload Enterprise Dataset (CSV, XLSX)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # High-Performance Data Loading
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        profile = get_detailed_profile(df)
        
        # SIDEBAR: DATA COMMAND CENTER
        with st.sidebar:
            st.header("🏥 Data Health Audit")
            c1, c2 = st.columns(2)
            c1.metric("Rows", profile["shape"][0])
            c2.metric("Nulls", profile["total_nulls"])
            
            st.markdown("---")
            st.subheader("🛠️ Self-Correction Engine")
            clean_action = st.selectbox("Intelligence Strategy", [
                "None", "Drop All Nulls", "Drop Duplicate Rows", 
                "Deep Fill Strategy", "Remove Outliers (Z-Score)", "Normalize Data"
            ])
            
            if clean_action != "None":
                df = smart_cleaner(df, clean_action)
                st.success(f"Strategy '{clean_action}' Applied")
                profile = get_detailed_profile(df) # Refresh profile

            st.markdown("---")
            if client:
                if st.button("🤖 Run AI Deep Audit"):
                    prompt = f"Analyze this data: {list(df.columns)}. Rows: {df.shape[0]}. Describe 3 key trends."
                    response = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.1-8b-instant" # Updated 2026 Workhorse
                    )
                    insight = response.choices[0].message.content
                    st.session_state.history.append({"time": time.ctime(), "insight": insight})
                    st.info(insight)

        # MAIN TABS SYSTEM
        tab_viz, tab_data, tab_ai = st.tabs(["🎨 Visual Studio", "📋 Data Explorer", "🧠 AI History"])
        
        with tab_viz:
            ctrl, view = st.columns([1, 3], gap="large")
            
            with ctrl:
                st.subheader("Chart Config")
                category = st.radio("Category", ["Relationship", "Comparison", "Distribution", "Composition", "Specialized"])
                
                # Dynamic Logic for 15+ Charts
                chart_map = {
                    "Relationship": ["Elite Scatter (4D)", "Bubble Relationship", "Interactive Heatmap"],
                    "Comparison": ["Professional Bar", "Line (Time-Series)", "Area (Stacked)"],
                    "Distribution": ["Advanced Violin", "Box Spread (Outliers)", "High-Density Histogram"],
                    "Composition": ["Sunburst (Radial)", "Tree Map (Hierarchical)", "Elite Pie"],
                    "Specialized": ["Spider/Radar Chart", "Parallel Categories", "Density Heatmap"]
                }
                
                chart_type = st.selectbox("Visual Engine", chart_map[category])
                
                # Smart Axis Filtering
                num_cols = [c for c, v in profile["columns"].items() if v["is_numeric"]]
                all_cols = list(df.columns)
                
                x_axis = st.selectbox("Primary Axis (X)", all_cols)
                y_axis = st.selectbox("Measure Axis (Y)", [None] + num_cols) # CRITICAL: Null filter
                color_dim = st.selectbox("Color Mapping", [None] + all_cols)
                
                size_dim = None
                if "Scatter" in chart_type or "Bubble" in chart_type:
                    size_dim = st.selectbox("Magnitude (Size)", [None] + num_cols)

            with view:
                # Execution of Elite Chart Engine
                fig = render_universal_chart(df, chart_type, x_axis, y_axis, color_dim, size_dim)
                if fig:
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
                
                st.download_button("📥 Export Cleaned Dataset", df.to_csv(index=False), "cleaned_data.csv")

        with tab_data:
            st.dataframe(df, use_container_width=True, height=600)
            
        with tab_ai:
            for item in reversed(st.session_state.history):
                st.write(f"**Audit at {item['time']}**")
                st.write(item['insight'])
                st.divider()

    except Exception as e:
        st.error(f"Universal Logic Failure: {str(e)}")
else:
    st.info("👋 Welcome. Please upload a dataset in the sidebar to begin the analysis.")