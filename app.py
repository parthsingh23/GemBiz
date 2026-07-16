import streamlit as st
import time

from streamlit_lottie import st_lottie
import requests

from utils.invoice_generator import (
    generate_invoice_number,
    generate_invoice_pdf,
    calculate_unit_price,
)
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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

LOTTIE_URL = "https://assets10.lottiefiles.com/packages/lf20_usmfx6bp.json"

try:
    animation = requests.get(LOTTIE_URL).json()
except:
    animation = None

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

try:

    sales_df = load_csv(
        sales_file,
        "sales"
    )

    inventory_df = load_csv(
        inventory_file,
        "inventory"
    )

    expenses_df = load_csv(
        expenses_file,
        "expenses"
    )

except Exception as e:

    st.error(str(e))
    st.stop()

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

m1.metric("💰 Revenue", f"Rs. {kpis['Revenue']:,.0f}")
m2.metric("📉 Expenses", f"Rs. {kpis['Expenses']:,.0f}")
m3.metric("📈 Profit", f"Rs. {kpis['Profit']:,.0f}")
m4.metric("📦 Inventory", f"{kpis['Inventory']}")
m5.metric("❤️ Health", f"{kpis['Health Score']}/100", kpis["Health Status"])

st.divider()

if sales_df is not None and inventory_df is not None and expenses_df is not None:

    left,right = st.columns(2)

    with left:
        st.plotly_chart(revenue_chart(sales_df), width="stretch")

    with right:
        st.plotly_chart(inventory_chart(inventory_df), width="stretch")

    left,right = st.columns(2)

    with left:
        st.plotly_chart(expense_chart(expenses_df), width="stretch")

    with right:
        st.plotly_chart(top_products_chart(sales_df), width="stretch")

    st.divider()

    placeholder = st.empty()

    try:

        with placeholder.container():

            if animation:
                st_lottie(
                    animation,
                    height=220,
                    key="loading",
                )

            st.info("🤖 GemBiz AI is analyzing your business...")

            report = generate_business_report(
                kpis,
                sales_df,
                inventory_df,
                expenses_df,
            )

        placeholder.empty()

        st.success("✅ Analysis Complete!")

        with st.container(border=True):
            st.markdown(report)

    except Exception as e:

        placeholder.empty()

        report = f"Unable to generate report.\n\n{e}"

        st.error(report)

        st.divider()

    # ======================================================
    # AI Chat
    # ======================================================

    st.divider()

    st.subheader("💬 Ask GemBiz AI")

    with st.container(border=True):

        st.caption(
            "Ask questions about your uploaded business data."
        )

        st.markdown("""
        **Try asking:**

        - Which product generates the most revenue?
        - How can I improve profit?
        - Which expense category is the highest?
        - Give me a business summary.
        """)

        question = st.text_area(
            "Ask your question",
            placeholder="Example: How can I improve my profit margin?",
            height=100,
        )

        ask = st.button(
            "🤖 Ask GemBiz",
            width="stretch",
        )

    for q, a in reversed(st.session_state.chat_history):
        
        with st.chat_message("user"):
            st.write(q)
        with st.chat_message("assistant"):
            st.write(a)

    if ask and question.strip():

        with st.status(
            "🤖 GemBiz AI is analyzing your question...",
            expanded=True,
        ) as status:

            st.write("📊 Reading uploaded business data...")
            time.sleep(0.4)

            st.write("🧠 Understanding your question...")
            time.sleep(0.4)

            st.write("💡 Consulting Google Gemma...")
            time.sleep(0.4)

            answer = ask_business_ai(
                question,
                kpis,
                sales_df,
                inventory_df,
                expenses_df,
            )

            status.update(
                label="✅ Response Ready",
                state="complete",
            )

        st.session_state.chat_history.append(
            (question, answer)
        )

        st.rerun()

        # for q, a in reversed(st.session_state.chat_history):
        
        #     with st.chat_message("user"):
        #         st.write(q)

        #     with st.chat_message("assistant"):
        #         st.write(a)

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
                width="stretch"
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
                f"Rs. {predicted:,.0f}"
            )

            st.metric(
                "Business Trend",
                trend
            )

            st.dataframe(
                forecast_df,
                width="stretch"
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
            width="stretch",
        )

        # ======================================================
        # Invoice Generator
        # ======================================================

        st.divider()

        st.subheader("🧾 Invoice Generator")

        if "invoice_number" not in st.session_state:
            st.session_state.invoice_number = generate_invoice_number()

        with st.container(border=True):

            st.caption(
                "Generate a professional invoice for your customer."
            )

            customer_name = st.text_input(
                "Customer Name"
            )

            customer_phone = st.text_input(
                "Customer Phone Number"
            )

            products = sorted(
                sales_df["Product"].unique()
            )

            selected_products = st.multiselect(
                "Select Product",
                products,
            )

            quantities = {}

            for product in selected_products:
            
                quantities[product] = st.number_input(
                    f"Quantity for {product}",
                    min_value=1,
                    value=1,
                    step=1,
                    key=f"qty_{product}",
                )

            st.info(
                f"Invoice Number: {st.session_state.invoice_number}"
            )

            generate_invoice = st.button(
                "🧾 Generate Invoice",
                width="stretch",
            )

        if generate_invoice:


            if not customer_name.strip():
                st.error("Enter customer name.")
                st.stop()

            if not customer_phone.strip():
                st.error("Enter customer phone number.")
                st.stop()

            if not customer_phone.isdigit():
                st.error("Phone number must contain digits only.")
                st.stop()

            if len(customer_phone) != 10:
                st.error("Phone number must be 10 digits.")
                st.stop()
        
            invoice_pdf = generate_invoice_pdf(
                invoice_number=st.session_state.invoice_number,
                customer_name=customer_name,
                customer_phone=customer_phone,
                products=selected_products,
                quantities=quantities,
                sales_df=sales_df,
            )

            st.success("✅ Invoice generated successfully!")

            st.download_button(
                label="📄 Download Invoice",
                data=invoice_pdf,
                file_name=f"{st.session_state.invoice_number}.pdf",
                mime="application/pdf",
                width="stretch",
            )

            # Show Invoice Preview
            st.divider()

            st.subheader("Invoice Preview")
            
            st.write(f"**Invoice No.:** {st.session_state.invoice_number}")
            st.write(f"**Customer:** {customer_name}")
            st.write(f"**Phone:** {customer_phone}")
            
            grand_total = 0
            
            for p in selected_products:
            
                unit_price = calculate_unit_price(
                    sales_df,
                    p,
                )
            
                qty = quantities[p]
            
                total = qty * unit_price
            
                grand_total += total
            
                st.write(
                    f"- {p} | Qty: {qty} | "
                    f"Rs. {unit_price:,.2f} | "
                    f"Rs. {total:,.2f}"
                )
            
            st.write(f"### Total: Rs. {grand_total:,.2f}")
            
            st.session_state.invoice_number = generate_invoice_number()

else:
    st.info(
        "Upload all three CSV files to unlock GemBiz."
    )

st.divider()

st.caption(
    "Built with ❤️ for Build with Gemma Hackathon | Google Gemma 4 | Streamlit | Plotly | Pandas"
)