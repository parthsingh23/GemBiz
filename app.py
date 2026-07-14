import streamlit as st

from utils.gemma_ai import generate_business_report
from utils.business_chat import ask_business_ai
from utils.pdf_generator import generate_pdf
from utils.parser import load_csv
from utils.analytics import calculate_kpis
from utils.prediction import forecast_sales
from utils.charts import (
    revenue_chart,
    inventory_chart,
    expense_chart,
    top_products_chart,
    forecast_chart,
)

st.set_page_config(
    page_title="GemBiz",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.title("💎 GemBiz")
    st.caption("AI-Powered Business Intelligence")
    st.divider()
    st.subheader("📂 Upload Business Data")

    sales_file = st.file_uploader("Sales CSV", type=["csv"])
    inventory_file = st.file_uploader("Inventory CSV", type=["csv"])
    expenses_file = st.file_uploader("Expenses CSV", type=["csv"])

    st.divider()

    if sales_file and inventory_file and expenses_file:
        st.success("All datasets uploaded successfully.")
    else:
        st.warning("Upload all three CSV files.")

sales_df = load_csv(sales_file)
inventory_df = load_csv(inventory_file)
expenses_df = load_csv(expenses_file)

kpis = calculate_kpis(
    sales_df,
    inventory_df,
    expenses_df
)

st.title("💎 GemBiz")

c1,c2,c3 = st.columns(3)
c1.success("🤖 AI Powered")
c2.success("📊 Business Analytics")
c3.success("📈 Forecast Ready")

st.markdown("""
### Your AI Business Copilot

Upload your Sales, Inventory and Expense data to receive:

- 📊 Interactive Business Dashboard
- 🤖 AI Generated Business Reports
- 💬 Ask Questions about your Business
- 📈 Revenue Forecasting
- 📄 Professional PDF Reports
""")

st.divider()

m1,m2,m3,m4,m5 = st.columns(5)

m1.metric("💰 Revenue", f"₹{kpis['Revenue']:,.0f}")
m2.metric("📉 Expenses", f"₹{kpis['Expenses']:,.0f}")
m3.metric("📈 Profit", f"₹{kpis['Profit']:,.0f}")
m4.metric("📦 Inventory", f"{kpis['Inventory']}")
m5.metric("❤️ Health", f"{kpis['Health Score']}/100", kpis["Health Status"])

st.divider()

if sales_df is not None and inventory_df is not None and expenses_df is not None:

    left,right = st.columns(2)

    with left:
        st.plotly_chart(revenue_chart(sales_df), use_container_width=True)

    with right:
        st.plotly_chart(inventory_chart(inventory_df), use_container_width=True)

    left,right = st.columns(2)

    with left:
        st.plotly_chart(expense_chart(expenses_df), use_container_width=True)

    with right:
        st.plotly_chart(top_products_chart(sales_df), use_container_width=True)

    st.divider()

    st.subheader("🧠 AI Business Report")

    try:
        report = generate_business_report(
            kpis,
            sales_df,
            inventory_df,
            expenses_df,
        )

        with st.container(border=True):
            st.markdown(report)

    except Exception as e:
        report = f"Unable to generate report.\n\n{e}"
        st.error(report)

    st.divider()

    st.subheader("💬 Ask GemBiz AI")

    question = st.text_input(
        "Ask anything about your business..."
    )

    if st.button("Ask AI") and question.strip():
        with st.spinner("GemBiz is thinking..."):
            answer = ask_business_ai(
                question,
                kpis,
                sales_df,
                inventory_df,
                expenses_df,
            )
        st.success(answer)

    st.divider()

    st.caption("Forecast generated using historical revenue trends.")

    st.subheader("📈 Revenue Forecast")

    forecast_df = forecast_sales(sales_df)

    if forecast_df is not None:

        col1,col2 = st.columns([3,1])

        with col1:
            st.plotly_chart(
                forecast_chart(
                    sales_df,
                    forecast_df
                ),
                use_container_width=True
            )

        with col2:
            predicted = forecast_df["Predicted Revenue"].mean()

            trend = (
                "📈 Increasing"
                if forecast_df.iloc[-1]["Predicted Revenue"] >
                forecast_df.iloc[0]["Predicted Revenue"]
                else "📉 Decreasing"
            )

            st.metric(
                "7-Day Avg Revenue",
                f"₹{predicted:,.0f}"
            )

            st.metric(
                "Business Trend",
                trend
            )

            st.dataframe(
                forecast_df,
                use_container_width=True
            )

        st.download_button(
            label="📄 Download Business Report",
            data=generate_pdf(
                kpis,
                report,
                forecast_df
            ),
            file_name="GemBiz_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

else:
    st.info(
        "Upload all three CSV files to unlock GemBiz."
    )

st.divider()

st.caption(
    "Built with ❤️ for Build with Gemma Hackathon | Google Gemma 4 | Streamlit | Plotly | Pandas"
)