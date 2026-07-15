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
You are a senior business consultant preparing a professional report for a small business owner.

Business Data

Revenue: Rs. {revenue:,.2f}
Expenses: Rs. {expenses:,.2f}
Profit: Rs. {profit:,.2f}
Inventory Units: {inventory}
Business Health Score: {health}/100

Top Selling Product:
{top_product}

Highest Expense Category:
{highest_expense}

Products Running Low:
{", ".join(low_stock)}

Write a professional business report.

The report MUST contain exactly these sections:

Business Summary

Strengths

Weaknesses

Risks

Actionable Recommendations

Formatting Rules:

• Use plain text only.
• Do NOT use Markdown.
• Do NOT use ** or __.
• Do NOT use # headings.
• Do NOT number sections.
• Use the section titles exactly as written.
• Under each section write 3–5 concise bullet points.
• Every bullet must begin with the bullet character (•).
• Keep recommendations practical.
• Do not write introductions or conclusions.
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
                config={
                    "temperature": 0.3,
                },
            )

            text = getattr(response, "text", None)

            if text and text.strip():

                print(f"✅ Using AI model: {model}")

                return text.strip()

        except Exception as e:

            print(f"❌ {model} failed: {e}")

            last_error = e

            continue

    # ------------------------------------------------
    # Final Fallback
    # ------------------------------------------------

    return f"""
Business Summary

• AI report could not be generated.

Strengths

• Revenue, expenses, inventory and forecast are still available.

Weaknesses

• AI service is currently unavailable.

Risks

• Business recommendations could not be generated.

Actionable Recommendations

• Please try generating the report again later.

Technical Details

• Last Error: {last_error}
"""