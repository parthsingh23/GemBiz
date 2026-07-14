import streamlit as st

# ----------------------------
# Page Configuration
# ----------------------------

st.set_page_config(
    page_title="Business Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.title("📊 Business Analyzer")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Analytics",
        "AI Report",
        "Forecast",
        "AI Chat"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Upload your business data to unlock AI-powered insights."
)

# ----------------------------
# Dashboard
# ----------------------------

if page == "Dashboard":

    st.title("📊 Business Analyzer")

    st.write(
        "Welcome! Upload your sales, expenses, and inventory data to generate business insights."
    )

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Revenue",
            "₹0"
        )

    with col2:
        st.metric(
            "Expenses",
            "₹0"
        )

    with col3:
        st.metric(
            "Profit",
            "₹0"
        )

    with col4:
        st.metric(
            "Business Health",
            "100%"
        )

    st.markdown("---")

    st.subheader("Getting Started")

    st.success(
        """
        Upload these files to begin:

        • Sales CSV

        • Inventory CSV

        • Expenses CSV
        """
    )

elif page == "Analytics":

    st.title("📈 Analytics")

    st.info("Analytics will appear here.")

elif page == "AI Report":

    st.title("🤖 AI Report")

    st.info("Gemma-generated report will appear here.")

elif page == "Forecast":

    st.title("📉 Forecast")

    st.info("Sales prediction module.")

elif page == "AI Chat":

    st.title("💬 AI Chat")

    st.info("Chat with your business data.")