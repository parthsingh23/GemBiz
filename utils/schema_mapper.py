import os
import json
import re

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def map_columns(df, dataset_type):

    if dataset_type == "sales":

        expected = [
            "Date",
            "Product",
            "Revenue"
        ]

    elif dataset_type == "inventory":

        expected = [
            "Product",
            "Stock",
            "Minimum Stock",
            "Supplier"
        ]

    elif dataset_type == "expenses":

        expected = [
            "Date",
            "Category",
            "Amount"
        ]

    else:

        return df

    # ============================================
    # NEW: Skip AI if the CSV already has
    # the expected columns
    # ============================================

    expected_set = set(expected)
    uploaded_set = set(df.columns)

    if expected_set.issubset(uploaded_set):
        return df

    # ============================================
    # Continue with AI mapping
    # ============================================

    columns = list(df.columns)

    sample = df.head(5).to_markdown(index=False)

    prompt = f"""
You are an expert data engineer.

A user uploaded a {dataset_type} CSV.

Expected columns:

{expected}

Uploaded columns:

{columns}

Sample rows:

{sample}

Your job is to match uploaded columns
to expected columns.

Return ONLY JSON.

Example:

{{
    "Date":"Invoice Date",
    "Product":"Item Name",
    "Revenue":"Sales Value"
}}

If an expected column
cannot be identified,
set its value to null.

Do NOT explain anything.

Return ONLY valid JSON.
"""

    # response = client.models.generate_content(
    #     model="gemma-4-31b-it",
    #     contents=prompt
    # )

    response = client.models.generate_content(
    model="gemma-4-31b-it",
    contents=prompt
    )

    print("========== GEMMA RESPONSE ==========")
    print(response.text)
    print("===================================")

    text = response.text.strip()

    # Remove markdown code blocks if present
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    mapping = json.loads(text)

    rename_dict = {}

    for expected_col, uploaded_col in mapping.items():

        if uploaded_col is not None:

            rename_dict[uploaded_col] = expected_col

    return df.rename(columns=rename_dict)