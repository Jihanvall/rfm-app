# 📊 Enterprise Customer Segmentation System

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)

##  Live Demo
**Check out the live application here:**
 **[Launch Customer Segmentation App](https://share.streamlit.io/jihanvall/rfm-app/main/app.py)**

---

## Project Overview
This project is an end-to-end **Machine Learning application** designed to help marketing teams optimize their campaigns. By analyzing raw sales data, the system automatically segments customers into distinct groups using **RFM Analysis** (Recency, Frequency, Monetary) and **Unsupervised Learning (K-Means Clustering)**.

###  Business Value
Instead of treating all customers the same, this tool enables businesses to:
* Identify **VIP Customers (Champions)** to reward loyalty.
* Detect **At-Risk Customers** before they churn.
* Target specific groups with personalized marketing strategies to increase ROI.

---

##  Key Features
* **Automated Data Cleaning:** Handles missing values and preprocesses raw transaction logs.
* **RFM Engine:** Calculates Recency, Frequency, and Monetary scores for every unique customer.
* **AI-Powered Segmentation:** Uses K-Means Clustering to group customers based on behavior, not just demographics.
* **Smart Recommendations:** Provides actionable marketing strategies (e.g., "Send discount", "Offer early access") based on the selected segment.
* **Interactive Dashboard:** Visualizes segment distribution and KPIs using Plotly.
* **Export Ready:** Allows users to download the segmented data as CSV for use in CRM tools.

---

##  Tech Stack
| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.9+ | Core logic and scripting. |
| **Frontend** | Streamlit | Web interface and interactivity. |
| **ML & Logic** | Scikit-Learn | K-Means Clustering algorithm. |
| **Data Processing** | Pandas & NumPy | Data manipulation and aggregation. |

---

## 📂 Project Structure
```text
rfm-app/
├── app.py                # Main Streamlit application
├── processor.py          # Data processing and ML logic
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
└── .gitignore            # Files excluded from version control
```
---

##  How to Run Locally
If you want to run this app on your own machine, follow these steps:

**1. Clone the repository:**
```bash
git clone [https://github.com/Jihanvall/rfm-app.git](https://github.com/Jihanvall/rfm-app.git)
cd rfm-app

## 2. install dependencies:
pip install -r requirements.txt

## 3.Run the app:
streamlit run app.py



