import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def map_columns(df, dataset_type):
    """
    Uses Gemma to map uploaded column names
    to GemBiz's expected schema.
    """

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

    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents=prompt
    )

    mapping = json.loads(response.text)

    rename_dict = {}

    for expected_col, uploaded_col in mapping.items():

        if uploaded_col is not None:

            rename_dict[uploaded_col] = expected_col

    return df.rename(columns=rename_dict)