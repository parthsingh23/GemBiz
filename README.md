# 💎 GemBiz

### AI-Powered Business Intelligence Platform for Small Businesses

GemBiz transforms raw business CSV files into actionable business insights using **Google Gemma 4**. Upload your sales, inventory, and expense data to instantly generate dashboards, forecasts, AI-generated reports, business recommendations, and professional invoices.

Built for the **Build with Gemma Hackathon**.

> 🚀 AI-Powered • Business Analytics • Forecasting • Smart Invoicing

---

# 📌 Problem Statement

Small businesses often manage their operations through spreadsheets.

While they possess valuable business data, extracting meaningful insights requires either expensive Business Intelligence software or technical expertise.

Business owners struggle to:

- 📈 Monitor sales performance
- 💰 Track profitability
- 📦 Manage inventory
- 📉 Forecast future revenue
- 📊 Make data-driven decisions

---

# 💡 Solution

GemBiz is an AI-powered Business Intelligence platform that converts ordinary CSV files into an intelligent business dashboard.

Simply upload:

- 📈 Sales Data
- 📦 Inventory Data
- 💰 Expense Data

GemBiz automatically:

- Cleans and standardizes data
- Maps different CSV schemas using Google Gemma
- Generates business KPIs
- Creates interactive visualizations
- Forecasts revenue
- Produces AI-generated business reports
- Answers business questions through an AI assistant
- Generates professional GST-style invoices

---

# ✨ Features

## 📊 Business Dashboard

- Revenue, Expenses & Profit KPIs
- Business Health Score
- Inventory Overview
- Top Selling Products
- Interactive Charts

---

## 🤖 AI-Powered CSV Understanding

Unlike traditional dashboards, GemBiz understands **different CSV formats**.

It automatically:

- Detects column mappings
- Handles inconsistent datasets
- Infers missing business fields
- Creates intelligent assumptions when possible

Powered by **Google Gemma 4**.

---

## 📈 Revenue Forecasting

- 7-Day Revenue Prediction
- Trend Analysis
- Forecast Visualization

---

## 🤖 AI Business Report

Generate an executive report containing:

- Business Summary
- Strengths
- Weaknesses
- Risks
- Actionable Recommendations

---

## 💬 AI Business Assistant

Ask natural language questions such as:

- Why is my profit decreasing?
- Which products should I restock?
- Which month performed the best?
- How can I improve revenue?

Powered by Google Gemma.

---

## 🧾 Smart Invoice Generator

Generate professional invoices with:

- Customer Details
- Multiple Product Selection
- Quantity Management
- Automatic Unit Price Calculation
- Discount Calculation
- GST Calculation
- Net Payable Amount
- Downloadable PDF Invoice

---

## 📄 PDF Business Report

Export a professionally formatted PDF containing:

- KPIs
- Charts
- AI Summary
- Business Recommendations

---

## ⚡ Performance Optimizations

- AI schema mapping cached using file hashing
- Prevents unnecessary API calls
- Faster dashboard updates
- Graceful fallback for malformed AI responses

---

# 🛠 Tech Stack

## Frontend

- Streamlit

## Backend

- Python

## AI

- Google Gemma 4
- Google GenAI SDK

## Data Processing

- Pandas
- NumPy

## Machine Learning

- Scikit-learn

## Visualization

- Plotly

## PDF Generation

- ReportLab

---

# 🏗 Architecture

```text
                 CSV Files
                     │
                     ▼
          AI Schema Detection
           (Google Gemma 4)
                     │
                     ▼
           Smart CSV Parser
                     │
                     ▼
          Data Standardization
                     │
                     ▼
          Business Analytics Engine
             │        │        │
             │        │        │
             ▼        ▼        ▼
        KPIs     Forecasts   Charts
             │
             ▼
        Google Gemma 4
             │
      ┌──────┼───────────┐
      ▼      ▼           ▼
 AI Report  AI Chat   PDF Export
                     │
                     ▼
             Invoice Generator
```

---

# 📂 Project Structure

```text
GemBiz/
│
├── app.py
├── assets/
├── data/
├── exports/
├── utils/
│   ├── analytics.py
│   ├── business_chat.py
│   ├── charts.py
│   ├── forecast.py
│   ├── gemma_ai.py
│   ├── invoice_generator.py
│   ├── parser.py
│   ├── pdf_generator.py
│   └── schema_mapper.py
│
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

```bash
git clone https://github.com/parthsingh23/GemBiz.git

cd GemBiz

python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

# 📂 Sample Datasets

Example CSV files are included inside the **data/** folder.

- sample_sales.csv
- sample_inventory.csv
- sample_expenses.csv

These can be used to explore the application without preparing your own datasets.

---

<!-- # 🎯 Future Scope

- Multi-user authentication
- Cloud database integration
- Automated inventory alerts
- Demand forecasting
- Sales anomaly detection
- Customer analytics
- GST & accounting software integration
- Real-time business monitoring
- WhatsApp & Email report delivery
- Multi-language AI assistant

--- -->

<!-- # 📸 Screenshots

> Add screenshots of:

- Dashboard
- Analytics
- AI Report
- AI Chat
- Revenue Forecast
- Invoice Generator

--- -->

# 🏆 Built For

**Build with Gemma Hackathon**

Powered by **Google Gemma 4**

---

# 👥 Team

**Team ByteForge**

### Members

- Rohan Shaw
- Khushbu Shaw
- Samiya Ali
- Parth Singh

---

# 📄 License

This project is licensed under the MIT License.