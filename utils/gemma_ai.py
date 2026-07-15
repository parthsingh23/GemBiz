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

Formatting Rules:

- Never use Markdown.
- Never use **, __, #, ##, ###.
- Never use numbered headings.
- Never write "BUSINESS ANALYSIS REPORT".
- Never wrap the response inside code blocks.
- Do not use markdown tables.

The report MUST contain ONLY these section headings exactly as written:

Business Summary

Strengths

Weaknesses

Risks

Actionable Recommendations

Formatting Example (follow exactly):

Business Summary

• Revenue has increased.
• Expenses remain high.
• Inventory levels are stable.

Strengths

• Strong demand for Coffee.
• Healthy inventory management.
• Consistent customer sales.

Weaknesses

• High operating expenses.
• Low profit margin.
• Heavy dependence on one product.

Risks

• Cash flow pressure.
• Supplier dependency.
• Rising operational costs.

Actionable Recommendations

• Reduce unnecessary expenses.
• Increase marketing for high-margin products.
• Diversify product offerings.

Rules:

- Leave ONE blank line after every heading.
- Every bullet MUST begin on a NEW LINE.
- Never place bullets on the same line as a heading.
- Never combine multiple bullets into one paragraph.
- Write exactly 3-5 bullet points per section.
- Keep every bullet concise and actionable.
- Do not add any introduction or conclusion.
"""

    models = [
    
        # ==========================
        # Gemma
        # ==========================
    
        "gemma-4-31b-it",
        "gemma-4-26b-a4b-it",
    
        # ==========================
        # Gemini 3.x
        # ==========================
    
        "gemini-3.5-flash",
    
        "gemini-3.1-pro-preview",
    
        "gemini-3-pro-preview",
    
        "gemini-3-flash-preview",
    
        "gemini-3.1-flash-lite",
    
        "gemini-3.1-flash-lite-preview",
    
        # ==========================
        # Gemini 2.5
        # ==========================
    
        "gemini-2.5-pro",
    
        "gemini-2.5-flash",
    
        "gemini-2.5-flash-lite",
    
        # ==========================
        # Gemini 2.0
        # ==========================
    
        "gemini-2.0-flash",
    
        "gemini-2.0-flash-lite",
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
                cleaned = cleaned.replace("\r\n", "\n")
                cleaned = cleaned.replace("\r", "\n")

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