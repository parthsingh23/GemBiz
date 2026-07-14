import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_business_ai(
    question,
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

    sales_data = (
        sales_df.head(20).to_string(index=False)
        if sales_df is not None
        else "No sales data"
    )

    inventory_data = (
        inventory_df.to_string(index=False)
        if inventory_df is not None
        else "No inventory data"
    )

    expenses_data = (
        expenses_df.to_string(index=False)
        if expenses_df is not None
        else "No expenses data"
    )

    prompt = f"""
You are GemBiz AI.

You are helping a small business owner.

Business KPIs

Revenue: ₹{revenue}

Expenses: ₹{expenses}

Profit: ₹{profit}

Inventory Units: {inventory}

Health Score: {health}/100

Sales Data

{sales_data}

Inventory Data

{inventory_data}

Expenses Data

{expenses_data}

User Question

{question}

Answer in simple business language.

Give practical recommendations.

Keep the answer under 250 words.
"""

    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents=prompt,
    )

    return response.text.strip()