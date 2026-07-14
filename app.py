import streamlit as st

from utils.parser import load_csv
from utils.analytics import calculate_kpis
from utils.charts import (
    revenue_chart,
    inventory_chart,
    expense_chart,
    top_products_chart
)

# ----------------------------------
# Page Configuration
# ----------------------------------

st.set_page_config(
    page_title="GemBiz",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------
# Sidebar
# ----------------------------------

with st.sidebar:

    st.title("💎 GemBiz")

    st.caption("AI-Powered Business Intelligence Platform")

    st.divider()

    st.subheader("📂 Upload Business Data")

    sales_file = st.file_uploader(
        "📈 Sales CSV",
        type=["csv"]
    )

    inventory_file = st.file_uploader(
        "📦 Inventory CSV",
        type=["csv"]
    )

    expenses_file = st.file_uploader(
        "💰 Expenses CSV",
        type=["csv"]
    )

    st.divider()

    if sales_file and inventory_file and expenses_file:
        st.success("✅ All files uploaded")
    else:
        st.warning("Upload all three CSV files")

# ----------------------------------
# Load Data
# ----------------------------------

sales_df = load_csv(sales_file)
inventory_df = load_csv(inventory_file)
expenses_df = load_csv(expenses_file)

kpis = calculate_kpis(
    sales_df,
    inventory_df,
    expenses_df
)

# ----------------------------------
# Dashboard Header
# ----------------------------------

st.title("💎 GemBiz")

st.caption(
    "AI-Powered Business Intelligence Platform for Small Businesses"
)

st.divider()

# ----------------------------------
# KPI Cards
# ----------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Revenue",
        f"₹{kpis['Revenue']:,.0f}"
    )

with col2:
    st.metric(
        "📉 Expenses",
        f"₹{kpis['Expenses']:,.0f}"
    )

with col3:
    st.metric(
        "📈 Profit",
        f"₹{kpis['Profit']:,.0f}"
    )

with col4:
    st.metric(
        "📦 Inventory",
        f"{kpis['Inventory']} Items"
    )

st.markdown("---")

# ----------------------------------
# Charts
# ----------------------------------

if sales_df is not None and inventory_df is not None and expenses_df is not None:

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.plotly_chart(
            revenue_chart(sales_df),
            use_container_width=True
        )

    with row1_col2:
        st.plotly_chart(
            inventory_chart(inventory_df),
            use_container_width=True
        )

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.plotly_chart(
            expense_chart(expenses_df),
            use_container_width=True
        )

    with row2_col2:
        st.plotly_chart(
            top_products_chart(sales_df),
            use_container_width=True
        )

else:

    st.info("📂 Upload all three CSV files to unlock analytics.")

st.markdown("---")

# ----------------------------------
# AI Insights
# ----------------------------------

st.subheader("🤖 AI Business Insights")

if sales_df is not None and inventory_df is not None and expenses_df is not None:

    st.success(
        """
Gemma AI has not been connected yet.

Soon this section will generate:

• Business Summary

• Sales Trends

• Inventory Alerts

• Expense Analysis

• Actionable Recommendations
"""
    )

else:

    st.info(
        "Upload your datasets to enable AI-powered business recommendations."
    )

st.markdown("---")

# ----------------------------------
# Forecast
# ----------------------------------

st.subheader("📈 Forecast")

st.info(
    "Sales forecasting and inventory prediction will appear here."
)

st.markdown("---")

st.caption(
    "💎 GemBiz • Built using Streamlit, Pandas, Plotly & Google Gemma"
)