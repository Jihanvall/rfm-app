import streamlit as st
import pandas as pd
import plotly.express as px
from processor import RFMSegmentationPipeline

# --- 1. Page Configuration ---
st.set_page_config(page_title="Customer Segmentation App", page_icon="🚀", layout="wide")

st.title("📊 Enterprise Customer Segmentation System")
st.markdown("**Upload your sales data** to unlock actionable insights.")
st.markdown("---")

# --- 2. File Uploader ---
uploaded_file = st.file_uploader("Choose a CSV file...", type=['csv'])

if uploaded_file is not None:
    try:
        with st.spinner('Processing Data... Please wait...'):
            # Initialize & Run Pipeline
            pipeline = RFMSegmentationPipeline(uploaded_file)
            final_df = pipeline.run()
            whales = pipeline.get_whales()
            
            # --- 🛠️ SAFETY FIX (إصلاح الخطأ) ---
            # If CustomerID is hidden in the index, bring it back as a column
            if 'CustomerID' not in final_df.columns:
                final_df = final_df.reset_index()
            # ----------------------------------
        
        st.success("Analysis Completed Successfully! ")
        
        # --- A. KPI Overview ---
        st.subheader("1.  Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Revenue", f"${final_df['Monetary'].sum():,.0f}")
        col2.metric("Total Customers", f"{len(final_df):,}")
        col3.metric("Champions (VIP)", len(final_df[final_df['Segment'] == 'Champions']))
        col4.metric("Avg Spend / User", f"${final_df['Monetary'].mean():,.0f}")
        
        st.markdown("---")

        # --- B. Segment Profiling ---
        st.subheader("2.  Segment Profiling")
        
        # Create Summary Table
        summary_table = final_df.groupby('Segment').agg({
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean',
            'CustomerID': 'count'  # Now this will work because we fixed the column above
        }).round(1).sort_values(by='Monetary', ascending=False)
        
        # Rename count column
        summary_table = summary_table.rename(columns={'CustomerID': 'Count'})
        
        col_table, col_chart = st.columns([1, 2])
        
        with col_table:
            st.write("##### Summary Statistics")
            st.dataframe(summary_table)
            st.caption("Note: Lower Recency is better. Higher Frequency & Monetary are better.")

        with col_chart:
            st.write("##### Customer Distribution")
            fig_pie = px.pie(final_df, names='Segment', title='Segment Size', 
                             color='Segment', 
                             color_discrete_map={
                                 "Champions": "#2ECC71", 
                                 "Potential_At_Risk": "#F1C40F", 
                                 "Lost_Low_Value": "#E74C3C"
                             })
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("---")

        # --- C. AI Strategic Recommendations ---
        st.subheader("3.  AI Strategic Recommendations")
        
        # 1. Dropdown Selection
        selected_segment = st.selectbox("Select a Segment to Analyze:", final_df['Segment'].unique())
        
        # 2. Filter Data based on selection
        filtered_df = final_df[final_df['Segment'] == selected_segment].sort_values(by='Monetary', ascending=False)
        
        # 3. Conditional Logic for Recommendations
        st.markdown(f"### Strategy for: **{selected_segment}**")
        
        if selected_segment == 'Champions':
            st.success("🌟 **Strategy:** Reward Loyalty! These are your best customers. Do not annoy them with discounts. Give them early access to new products.")
        elif selected_segment == 'Potential_At_Risk':
            st.warning("⚠️ **Strategy:** Reactivation Required! They used to buy, but stopped. Send a 'We Miss You' email with a time-limited coupon.")
        else:
            st.error("📉 **Strategy:** Cost Control. Don't spend paid ads here. Use free channels (Email/Push) to try and bring them back.")

        # 4. Show Top 10 Customers in this segment
        st.write(f"**Top 10 High-Value Customers in '{selected_segment}':**")
        st.dataframe(filtered_df.head(10))

        st.markdown("---")
        
        # --- D. Export Section ---
        st.subheader("4. 📥 Export Data")
        csv = final_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Full Report (CSV)", csv, "segmentation_results.csv", "text/csv")

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Waiting for file upload...")