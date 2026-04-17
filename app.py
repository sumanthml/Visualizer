import streamlit as st
import pandas as pd
import numpy as np
from src.processor import get_detailed_profile, smart_cleaner
from src.charts import render_universal_chart
from groq import Groq
import time

# 1. GLOBAL UI CONFIGURATION (Ultra-Modern Glassmorphism Theme)
st.set_page_config(
    page_title="Universal Visualizer Ultra",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Injection for Elite UX
st.markdown("""
    <style>
    .main { 
        background-color: #0e1117; 
    }
    .stMetric { 
        background: rgba(255, 255, 255, 0.05); 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid rgba(255, 255, 255, 0.1); 
    }
    .stButton>button { 
        width: 100%; 
        border-radius: 5px; 
        background: linear-gradient(45deg, #FF4B4B, #FF8F8F); 
        border: none; 
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ZERO-COST AI ORCHESTRATION (Groq + Llama 3.1)
def initialize_ai():
    if "GROQ_API_KEY" in st.secrets:
        return Groq(api_key=st.secrets["GROQ_API_KEY"])
    return None

client = initialize_ai()

# 3. CORE LOGIC & DASHBOARD HEADER
st.title("🛡️ Universal Visualizer Ultra")
st.markdown("---")

# Persistent state management for history tracking
if "history" not in st.session_state:
    st.session_state.history = []

# Elite File Ingestion Layer
with st.container():
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        uploaded_file = st.file_uploader("Drop Enterprise Dataset (CSV, XLSX)", type=["csv", "xlsx"])
    with c2:
        st.info("💡 Pro Tip: Use the AI Deep Audit after cleaning for better insights.")

if uploaded_file:
    # High-Performance Data Loading
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # 4. INTELLIGENCE LAYER (Instant Profiling)
        profile = get_detailed_profile(df)
        
        # 5. SIDEBAR: DATA COMMAND CENTER
        with st.sidebar:
            st.image("https://img.icons8.com/fluency/96/000000/data-configuration.png", width=80)
            st.header("🏥 Health Center")
            
            # Interactive Health Metrics
            m1, m2 = st.columns(2)
            m1.metric("Total Rows", profile["shape"][0])
            m2.metric("Total Nulls", profile["total_nulls"])
            
            st.markdown("---")
            st.subheader("🛠️ Self-Correction Engine")
            
            # Multi-Strategy Cleaning Dashboard
            clean_action = st.selectbox("Intelligence Strategy", [
                "None", 
                "Drop All Nulls", 
                "Drop Duplicate Rows", 
                "Deep Fill Strategy", 
                "Remove Outliers (Z-Score)",
                "Normalize Data (Scaling)"
            ])
            
            if clean_action != "None":
                with st.spinner("Processing..."):
                    df = smart_cleaner(df, clean_action)
                    st.success(f"Action '{clean_action}' Applied!")
                    # Refresh profile after cleaning
                    profile = get_detailed_profile(df)

            st.markdown("---")
            st.subheader("🤖 AI Data Analyst")
            if client:
                if st.button("🚀 Run AI Deep Audit"):
                    with st.status("Analyzing Dataset Soul...", expanded=True) as status:
                        prompt = f"As a Senior Data Scientist, analyze this dataset profile: {list(df.columns)}. Focus on missing values ({profile['total_nulls']}) and suggest 3 strategic visualizations."
                        
                        response = client.chat.completions.create(
                            messages=[{"role": "user", "content": prompt}],
                            model="llama-3.1-8b-instant"
                        )
                        analysis = response.choices[0].message.content
                        st.write(analysis)
                        status.update(label="Audit Complete!", state="complete", expanded=False)
                        st.session_state.history.append({"time": time.ctime(), "insight": analysis})
            else:
                st.warning("AI Insights disabled: Key missing.")

        # 6. MAIN VISUALIZATION GALLERY (15+ Chart Engine)
        tabs = st.tabs(["🎨 Visual Studio", "📋 Data Explorer", "🧠 AI History"])
        
        with tabs[0]:
            st.subheader("Chart Designer Ultra")
            ctrl, view = st.columns([1, 3])
            
            with ctrl:
                # Elite Category Mapping
                chart_group = st.radio("Chart Category", ["Relationship", "Comparison", "Distribution", "Composition", "Specialized"])
                
                # Dynamic Filtering based on Category
                if chart_group == "Relationship":
                    charts = ["Elite Scatter (4D)", "Bubble Relationship", "Interactive Heatmap", "Density Heatmap"]
                elif chart_group == "Comparison":
                    charts = ["Professional Bar", "Line (Time-Series)", "Area (Stacked)", "Radar Chart"]
                elif chart_group == "Distribution":
                    charts = ["Advanced Violin", "Box Spread (Outliers)", "High-Density Histogram"]
                elif chart_group == "Composition":
                    charts = ["Sunburst (Radial)", "Tree Map (Hierarchical)", "Elite Pie"]
                else:
                    charts = ["Parallel Categories", "Spider/Radar Chart"]

                chart_choice = st.selectbox("Select Visual Engine", charts)
                st.markdown("---")
                
                # Smart Axis Mapping (Filters for DType Compatibility)
                x_col = st.selectbox("Primary Axis (X)", df.columns)
                num_cols = [c for c, v in profile["columns"].items() if v["is_numeric"]]
                cat_cols = [c for c, v in profile["columns"].items() if not v["is_numeric"]]
                
                y_col = st.selectbox("Measure Axis (Y)", [None] + num_cols)
                color_col = st.selectbox("Dimension Mapping (Color)", [None] + list(df.columns))
                
                # Advanced Controls for specialized charts
                size_col = None
                if "Scatter" in chart_choice or "Bubble" in chart_choice:
                    size_col = st.selectbox("Magnitude (Size)", [None] + num_cols)
                
                facet_col = st.selectbox("Sub-Plot (Facet)", [None] + cat_cols)

            with view:
                # Execution of the Elite Rendering Engine
                fig = render_universal_chart(df, chart_choice, x_col, y_col, color_col, size_col, facet_col)
                if fig:
                    st.plotly_chart(fig, use_container_width=True, theme=None)
                
                # Instant Export Layer
                col_down1, col_down2 = st.columns(2)
                col_down1.download_button("📥 Export Cleaned Data", df.to_csv(index=False), "cleaned_data.csv", "text/csv")
                
        with tabs[1]:
            st.subheader("Raw Intelligence Feed")
            st.dataframe(df, use_container_width=True)
            
        with tabs[2]:
            st.subheader("AI Insight Audit Log")
            for item in reversed(st.session_state.history):
                with st.expander(f"Audit from {item['time']}"):
                    st.write(item['insight'])

    except Exception as e:
        st.error(f"🚨 Universal Loader Error: {str(e)}")
        st.info("Check if your file format is corrupted or has illegal headers.")
else:
    # Splash Screen for Empty State
    st.image("https://img.icons8.com/clouds/200/000000/data-configuration.png")
    st.header("Welcome to Visualizer Ultra")
    st.write("Upload a dataset to activate the intelligence engine.")