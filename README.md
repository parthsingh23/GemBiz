# 💎 GemBiz

### AI-Powered Business Intelligence Platform for Small Businesses

GemBiz transforms raw business CSV files into actionable insights using
**Google Gemma**, interactive dashboards, forecasting, and AI-powered
business recommendations.

Built for the **Build with Gemma Hackathon**.

> **Status:** 🚀 Hackathon Submission

------------------------------------------------------------------------

## 📌 Problem Statement

Small businesses often manage sales, inventory, and expenses using
spreadsheets. While the data exists, extracting meaningful insights
usually requires expensive BI software or technical expertise.

As a result, business owners struggle to: - Track profitability -
Monitor inventory efficiently - Forecast future sales - Make data-driven
decisions

------------------------------------------------------------------------

## 💡 Solution

GemBiz is an AI-powered Business Intelligence platform that converts
simple CSV files into interactive dashboards, AI-generated reports,
forecasts, and downloadable PDF summaries.

Users only need to upload three CSV files:

-   📈 Sales Data
-   📦 Inventory Data
-   💰 Expense Data

GemBiz handles the analysis automatically.

------------------------------------------------------------------------

## ✨ Features

-   📊 Interactive Business Dashboard
-   💰 Revenue, Expenses & Profit KPIs
-   ❤️ Business Health Score
-   📦 Inventory Analytics
-   📈 Revenue Trend Visualization
-   🛒 Top Selling Products Analysis
-   🤖 AI Business Report powered by Google Gemma
-   💬 AI Business Chat Assistant
-   📈 7-Day Revenue Forecast
-   📄 Professional PDF Report Export
-   🔁 Automatic AI Model Fallback

------------------------------------------------------------------------

## 🛠 Tech Stack

### Frontend

-   Streamlit

### Backend

-   Python

### AI

-   Google Gemma 4
-   Google GenAI SDK

### Data Processing

-   Pandas
-   NumPy

### Machine Learning

-   Scikit-learn

### Visualization

-   Plotly

### PDF Generation

-   ReportLab

------------------------------------------------------------------------

## 🏗 Architecture

``` text
CSV Files
     │
     ▼
CSV Parser
     │
     ▼
Analytics Engine
     │
     ├── KPI Calculator
     ├── Forecast Model
     ├── Plotly Charts
     └── Google Gemma AI
             │
             ▼
 AI Report + AI Chat + PDF Export
```

------------------------------------------------------------------------

## 📂 Project Structure

``` text
GemBiz
│
├── app.py
├── assets/
├── data/
├── docs/
├── uploads/
├── exports/
├── utils/
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

## 🚀 Installation

``` bash
git clone https://github.com/parthsingh23/businessAnalyzer.git

cd businessAnalyzer

python -m venv venv

source venv/bin/activate   # Linux/macOS
# OR
venv\Scripts\activate      # Windows

pip install -r requirements.txt

streamlit run app.py
```

------------------------------------------------------------------------

## 🔑 Environment Variables

Create a `.env` file in the project root.

``` env
GEMINI_API_KEY=YOUR_API_KEY
```

------------------------------------------------------------------------

## 📂 Sample Dataset

Sample CSV files are included in the `data/` folder:

-   sample_sales.csv
-   sample_inventory.csv
-   sample_expenses.csv

------------------------------------------------------------------------

## 🚀 Future Scope

-   Multi-user authentication
-   Cloud database integration
-   Smart inventory alerts
-   Demand forecasting
-   Sales anomaly detection
-   GST & accounting integration
-   Real-time business monitoring

------------------------------------------------------------------------

## 📄 License

This project is licensed under the MIT License.

------------------------------------------------------------------------

## 👨‍💻 Developer

**Parth Singh**

Built for the **Build with Gemma Hackathon** using Google Gemma,
Streamlit, Plotly, and Python.
