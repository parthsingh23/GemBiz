import os

from dotenv import load_dotenv
from google import genai

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Check your .env file."
    )

client = genai.Client(api_key=API_KEY)

# ==========================================================
# Helper Functions
# ==========================================================


def get_top_product(sales_df):

    if sales_df is None or sales_df.empty:
        return "Unknown"

    try:

        return (
            sales_df.groupby("Product")["Revenue"]
            .sum()
            .idxmax()
        )

    except Exception:

        return "Unknown"


def get_highest_expense(expenses_df):

    if expenses_df is None or expenses_df.empty:
        return "Unknown"

    try:

        return (
            expenses_df.groupby("Category")["Amount"]
            .sum()
            .idxmax()
        )

    except Exception:

        return "Unknown"


def get_low_stock(inventory_df):

    if inventory_df is None or inventory_df.empty:
        return ["None"]

    try:

        products = inventory_df[
            inventory_df["Stock"]
            <=
            inventory_df["Minimum Stock"]
        ]["Product"].tolist()

        return products if products else ["None"]

    except Exception:

        return ["Unknown"]


# ==========================================================
# Generate Business Report
# ==========================================================


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

    top_product = get_top_product(sales_df)

    highest_expense = get_highest_expense(expenses_df)

    low_stock = get_low_stock(inventory_df)

    prompt = f"""
You are a Senior Business Consultant.

Prepare a professional business report.

Business Metrics

Revenue : Rs. {revenue:,.2f}

Expenses : Rs. {expenses:,.2f}

Profit : Rs. {profit:,.2f}

Inventory Units : {inventory}

Business Health Score : {health}/100

Top Selling Product

{top_product}

Highest Expense Category

{highest_expense}

Products Running Low

{", ".join(low_stock)}

Return ONLY plain text.

Never use Markdown.

Never use:

**

__

#

1.

2.

3.

BUSINESS ANALYSIS REPORT

Do not wrap text inside code blocks.

The report MUST contain ONLY these sections:

Business Summary

Strengths

Weaknesses

Risks

Actionable Recommendations

Under every section write exactly 3-5 bullet points.

Every bullet MUST start with:

•

No introductions.

No conclusions.

No markdown tables.

Keep recommendations practical.
"""

    models = [

        "gemma-4-31b-it",

        "gemma-4-26b-a4b-it",

        "gemini-3.5-flash",

    ]

    last_error = None

    for model in models:

        try:

            print(f"Trying model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            text = getattr(response, "text", None)

            if text:

                cleaned = text.strip()

                if cleaned:

                    print(f"Using AI model: {model}")

                    return cleaned

        except Exception as e:

            print(f"{model} failed")

            print(e)

            last_error = e

            continue

    print("All models failed.")

    return f"""
Business Summary

• AI report could not be generated.

Strengths

• Business analytics were generated successfully.

• KPI calculations remain available.

Weaknesses

• AI service is currently unavailable.

• Automated recommendations could not be produced.

Risks

• Strategic insights are unavailable until AI services recover.

• Business decisions should rely on dashboard metrics for now.

Actionable Recommendations

• Try generating the report again.

• Check your API key and internet connection.

• Retry after a few minutes.

Technical Details

Last Error:

{last_error}
"""