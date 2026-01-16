import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

class RFMSegmentationPipeline:
    """
    A production-grade class to handle the end-to-end RFM Segmentation process.
    """

    def __init__(self, file_path):
        # Changed to accept the actual raw data file path
        self.file_path = file_path
        self.data = None
        self.rfm = None
        self.model = None
        self.scaler = StandardScaler()

    def load_and_clean(self):
        # Check if it's a Streamlit file (has 'seek') or a normal path string
        is_streamlit_file = hasattr(self.file_path, 'seek')

        # 1. Try reading as standard UTF-8 
        try:
            if is_streamlit_file: self.file_path.seek(0)  
            df = pd.read_csv(self.file_path)
        except:
            # 2. Fallback: Try ISO-8859-1 (Best for the original Retail dataset)
            if is_streamlit_file: self.file_path.seek(0)  # REWIND AGAIN
            df = pd.read_csv(self.file_path, encoding="ISO-8859-1")
            
        # Basic cleaning
        df = df.dropna(subset=['CustomerID'])
        df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
        df['Total_Price'] = df['Quantity'] * df['UnitPrice']
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        
        self.data = df
        return self.data

        # Basic cleaning
        df = df.dropna(subset=['CustomerID'])
        df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
        df['Total_Price'] = df['Quantity'] * df['UnitPrice']
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

        self.data = df
        print("   Data Loaded Successfully.")

    def calculate_rfm(self):
        print("2. Calculating RFM Metrics...")
        reference_date = self.data['InvoiceDate'].max() + pd.Timedelta(days=1)

        self.rfm = self.data.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (reference_date - x.max()).days,
            'InvoiceNo': 'count',
            'Total_Price': 'sum'
        }).rename(columns={
            'InvoiceDate': 'Recency',
            'InvoiceNo': 'Frequency',
            'Total_Price': 'Monetary'
        })
        print("   RFM Table Created.")

    def preprocess_and_train(self, n_clusters=3):
        print(f"3. Training K-Means Model (k={n_clusters})...")

        # Log Transformation
        rfm_log = np.log1p(self.rfm)

        # Scaling
        rfm_scaled = self.scaler.fit_transform(rfm_log)

        # Modeling
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

        # --- Dynamic Mapping (Smart Step) ---
        # Instead of hardcoding 0, 1, 2, we sort them by Money.
        # The cluster with the most Money gets the 'Champions' label automatically.
        means = self.rfm.groupby('Cluster')['Monetary'].mean().sort_values(ascending=False)

        mapping = {
            means.index[0]: 'Champions',        # Highest Spenders
            means.index[1]: 'Potential_At_Risk',# Middle
            means.index[2]: 'Lost_Low_Value'    # Lowest
        }

        self.rfm['Segment'] = self.rfm['Cluster'].map(mapping)
        print("   Model Trained & Segments Assigned.")

    def get_whales(self, threshold=10000):
        print("4. Extracting Whales...")
        whales = self.rfm[self.rfm['Monetary'] > threshold].sort_values(by='Monetary', ascending=False)
        return whales

    def export_results(self, output_name='Production_Results.csv'):
        print(f"5. Saving Results to {output_name}...")
        final_df = self.rfm.reset_index()
        final_df.to_csv(output_name, index=False)
        print("   Done.")

    def run(self):
        """Orchestrates the whole pipeline"""
        self.load_and_clean()
        self.calculate_rfm()
        self.preprocess_and_train(n_clusters=3)
        self.export_results()
        return self.rfm

# --- EXECUTION ---
# This is how you run the code now (Clean & Simple):
if __name__ == "__main__":
    # Initialize the Pipeline with the path to the original Excel file
    pipeline = RFMSegmentationPipeline('/content/data/Online Retail.xlsx')

    # Run everything
    final_data = pipeline.run()

    # Print the Whales Report
    print("\n--- WHALE REPORT ---")
    print(pipeline.get_whales().head())