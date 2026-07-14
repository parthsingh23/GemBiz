import os

from dotenv import load_dotenv
from google import genai

# ----------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "❌ GEMINI_API_KEY not found. Please check your .env file."
    )

client = genai.Client(api_key=API_KEY)

# ----------------------------------------------------
# Generate Business Report
# ----------------------------------------------------

def generate_business_report(
    kpis,
    sales_df,
    inventory_df,
    expenses_df,
):

    revenue = kpis["Revenue"]
    expenses = kpis["Expenses"]
    profit = kpis["Profit"]
    inventory = kpis["Inventory"]
    health = kpis["Health Score"]

    # ------------------------------------------------
    # Top Selling Product
    # ------------------------------------------------

    if sales_df is not None and not sales_df.empty:

        top_product = (
            sales_df.groupby("Product")["Revenue"]
            .sum()
            .idxmax()
        )

    else:

        top_product = "Unknown"

    # ------------------------------------------------
    # Highest Expense Category
    # ------------------------------------------------

    if expenses_df is not None and not expenses_df.empty:

        highest_expense = (
            expenses_df.groupby("Category")["Amount"]
            .sum()
            .idxmax()
        )

    else:

        highest_expense = "Unknown"

    # ------------------------------------------------
    # Low Stock Products
    # ------------------------------------------------

    low_stock = []

    if inventory_df is not None and not inventory_df.empty:

        low_stock = inventory_df[
            inventory_df["Stock"]
            <=
            inventory_df["Minimum Stock"]
        ]["Product"].tolist()

    if not low_stock:
        low_stock = ["None"]

    # ------------------------------------------------
    # Prompt
    # ------------------------------------------------

    prompt = f"""
You are an expert Business Consultant.

Analyze the following business.

Revenue: ₹{revenue:,.2f}

Expenses: ₹{expenses:,.2f}

Profit: ₹{profit:,.2f}

Inventory Units: {inventory}

Business Health Score: {health}/100

Top Selling Product:
{top_product}

Highest Expense Category:
{highest_expense}

Products Running Low:
{", ".join(low_stock)}

Generate a professional business report using the following headings:

1. Business Summary

2. Strengths

3. Weaknesses

4. Risks

5. Actionable Recommendations

Rules:
- Keep the report concise.
- Use bullet points.
- Do NOT use markdown tables.
- Be practical and business-focused.
"""

    # ------------------------------------------------
    # AI Model Fallback Chain
    # ------------------------------------------------

    models = [
        "gemma-4-31b-it",
        "gemma-4-26b-a4b-it",
        "gemini-3.5-flash",
    ]

    last_error = None

    for model in models:

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            if response.text:

                print(f"Using AI model: {model}")

                return response.text.strip()

        except Exception as e:

            last_error = e

            continue

    raise RuntimeError(
        "All AI models are currently unavailable.\n\n"
        f"Last Error: {last_error}"
    )