import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime as dt
import joblib
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Insight AI Production",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS CUSTOM STYLING ---
st.markdown("""
<style>
    /* 1. GLOBAL TEXT COLOR & BACKGROUND ANIMATION */
    .stApp {
        background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #ffffff);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        
    }

    /* 2. REMOVE TOP WHITE SPACE (The "Big White Thing Above") */
    .block-container {
        padding-top: 0rem !important; /* Reduces top padding to zero */
        margin-top: 0rem !important;
    }

    /* Hiding standard Streamlit header elements completely */
    header[data-testid="stHeader"] {
        display: none;
    }
    #MainMenu {visibility: hidden; display: none;}
    footer {visibility: hidden; display: none;}

    /* 3. ANIMATION KEYFRAMES */
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* 4. METRICS STYLING */
    [data-testid="stMetric"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        justify-content: center;
    }
    [data-testid="stMetricValue"] {
        display: flex;
        justify-content: center;
        width:100%;
        font-size: 2.8rem !important;
        font-weight: 800;
        color: #fff !important;
    }
    [data-testid="stMetricLabel"] {
        display: flex;
        width: 100%;
        justify-content: center;
        font-size: 1.1rem !important;
        color: #fff !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        text-align: center;
        margin: auto;
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.3s ease-in-out;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        background-color: rgba(255, 255, 255, 0.2);
    }

    /* --- 8. CUSTOM FILE UPLOADER STYLING --- */

    /* 1. The "Small Box" (Drag & Drop Area) */
    [data-testid='stFileUploader'] section {
        background-color: rgba(0, 0, 0, 0.6) !important; /* Dark transparent background */
        border: 2px dashed rgba(255, 255, 255, 0.5) !important; /* White dashed border */
        color:black,
    }
            

    /* 2. The "Browse files" Button */
    [data-testid='stFileUploader'] section > button {
        background-color: white !important; /* Black Button */
        color: white !important;            /* White Text */
        border: 1px solid white !important; /* White Border */
    }

    /* 3. Button Hover Effect */
    [data-testid='stFileUploader'] section > button {
        background-color: #333 !important;  /* Dark Grey on Hover */
        color: #e73c7e !important;          /* Pink Text on Hover */
        border-color: #e73c7e !important;
    }

    /* 4. Text Color inside the Box ("Drag and drop file here") */
    [data-testid='stFileUploader'] section span, 
    [data-testid='stFileUploader'] section small, 
    [data-testid='stFileUploader'] section div {
         /* Force all text to be White */
            color: pink !important;
    }   

    /* 5. CUSTOM HEADER CLASS */
    .header-center {
        text-align: center;
        color: white;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 40px;
        margin-top: 20px; /* Added a little top margin for spacing */
        text-shadow: 0px 5px 15px rgba(0,0,0,0.3);
        font-family: 'Arial', sans-serif;
    }

    /* 6. BUTTONS */
    .stButton button {
        background: white;
        color: #e73c7e;
        border-radius: 30px;
        font-weight: bold;
        border: 2px solid #e73c7e;
        padding: 10px 25px;
        transition: 0.3s;
    }
    .stButton button:hover {
        background: #e73c7e;
        color: white;
    }

    /* 7. TABS STYLING */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
        width: 100%;
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border-radius: 10px;
        padding: 10px 30px;
        color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 700 !important;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-bottom: 3px solid white !important;
        font-weight: 900 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. ROBUST DATA PROCESSING ENGINE ---
def process_data_production(df):
    df.columns = [str(col).lower().strip() for col in df.columns]
    date_col = next((c for c in df.columns if 'date' in c or 'time' in c), None)
    id_col = next((c for c in df.columns if 'id' in c or 'cust' in c), None)
    amount_col = next((c for c in df.columns if 'amount' in c or 'total' in c or 'sales' in c), None)
    qty_col = next((c for c in df.columns if 'qty' in c or 'quantity' in c), None)
    price_col = next((c for c in df.columns if 'price' in c or 'unit' in c), None)

    if not date_col or not id_col:
        return None, "Error: Could not identify Customer ID or Date columns."

    df = df.dropna(subset=[id_col, date_col])
    
    if amount_col:
        df['monetary_val'] = pd.to_numeric(df[amount_col], errors='coerce')
    elif qty_col and price_col:
        df['monetary_val'] = pd.to_numeric(df[qty_col], errors='coerce') * pd.to_numeric(df[price_col], errors='coerce')
    else:
        return None, "Error: Could not calculate transaction values."

    df = df[df['monetary_val'] > 0]
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=['monetary_val', date_col])

    snapshot_date = df[date_col].max() + dt.timedelta(days=1)
    rfm = df.groupby(id_col).agg({
        date_col: lambda x: (snapshot_date - x.max()).days,
        id_col: 'count',
        'monetary_val': 'sum'
    }).rename(columns={date_col: 'Recency', id_col: 'Frequency', 'monetary_val': 'Monetary'})

    try:
        if not os.path.exists('scaler.pkl') or not os.path.exists('kmeans_model.pkl'):
            return None, "Model files missing."
        
        scaler = joblib.load('scaler.pkl')
        model = joblib.load('kmeans_model.pkl')
        
        input_features = rfm[['Recency', 'Frequency', 'Monetary']]
        rfm_log = np.log1p(input_features)
        rfm_scaled = scaler.transform(rfm_log)
        rfm['Cluster'] = model.predict(rfm_scaled)
        
        means = rfm.groupby('Cluster')['Monetary'].mean().sort_values(ascending=False)
        mapping = {means.index[0]: 'Champions', means.index[1]: 'Potential_At_Risk', means.index[2]: 'Lost_Low_Value'}
        for idx in range(3, len(means)): mapping[means.index[idx]] = f'Segment_{idx}'
        
        rfm['Segment'] = rfm['Cluster'].map(mapping)
        return rfm.reset_index(), None
    except Exception as e:
        return None, f"AI Engine Error: {str(e)}"

# --- 4. DASHBOARD INTERFACE ---
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

if st.session_state.processed_data is None:
    st.markdown('<div class="header-center">Upload Customer Data</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_file = st.file_uploader("", type=['csv', 'xlsx'])
        if uploaded_file:
            try:
                raw_df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                with st.spinner("AI Analyzing Patterns..."):
                    result_df, error = process_data_production(raw_df)
                    if error: st.error(error)
                    else:
                        st.session_state.processed_data = result_df
                        st.rerun()
            except Exception as e: st.error(f"File Loading Error: {e}")
else:
    df = st.session_state.processed_data
    
    # 1. HEADER & RESET BUTTON
    st.markdown('<div class="header-center">AI Customer Matrix</div>', unsafe_allow_html=True)
    
    col_spacer, col_btn = st.columns([5, 1])
    with col_btn:
        if st.button("🔄 New Analysis"):
            st.session_state.processed_data = None
            st.rerun()

    # 2. METRICS (ALWAYS SHOWS FULL DATA)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Revenue", f"${df['Monetary'].sum():,.0f}")
    m2.metric("Total Customers", len(df))
    m3.metric("Champions", len(df[df['Segment'] == 'Champions']))
    m4.metric("At Risk", len(df[df['Segment'] == 'Potential_At_Risk']))

    st.markdown("---")

    # 3. TABS (Visuals = Full Data | Table = Filtered)
    tab1, tab2 = st.tabs([" Global Analytics", "Customer Ledger"])
    
    # TAB 1: VISUALIZATIONS (UNFILTERED)
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            fig_pie = px.pie(df, names='Segment', values='Monetary', hole=0.5, template="plotly_dark", title="Total Revenue Share")
            st.plotly_chart(fig_pie, use_container_width=True)
        with c2:
            fig_scatter = px.scatter(df, x="Recency", y="Frequency", color="Segment", size="Monetary", template="plotly_dark", title="All Customers Distribution")
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    # TAB 2: TABLE WITH EXCLUSIVE FILTER
    with tab2:
        # --- FILTER MOVED INSIDE THIS TAB ---
        
        all_segments = df['Segment'].unique().tolist()
        
        # This filter ONLY affects 'table_df'
        st.markdown("""
            <h3 style='
                text-align: center; 
                color: white; 
                font-size: 26px; 
                font-weight: 800;
                margin-bottom: 10px;
            '>
                Select segments to view in table:
            </h3>
        """, unsafe_allow_html=True)


        selected_segments = st.multiselect(
            "Select segments:", 
            options=all_segments, 
            default=all_segments,
            label_visibility="collapsed"
        )
        
        # Filter Logic applies ONLY here
        table_df = df[df['Segment'].isin(selected_segments)]
        
        
        st.markdown(f"""
            <div style='
                text-align: center; 
                color: white; 
                font-size: 28px; 
                font-weight: 800; 
                padding: 15px; 
                border: 2px solid rgba(255,255,255,0.2); 
                border-radius: 10px;
                margin-bottom: 20px;
                background-color: rgba(255,255,255,0.05);
            '>
                Showing {len(table_df)} Rows
            </div>
        """, unsafe_allow_html=True)
        st.dataframe(table_df, use_container_width=True)
