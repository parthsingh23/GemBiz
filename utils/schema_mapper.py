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
            "Revenue",
            "Units Sold"
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

        return df, {}

    # ============================================
    # NEW: Skip AI if the CSV already has
    # the expected columns
    # ============================================

    expected_set = set(expected)
    uploaded_set = set(df.columns)

    if expected_set.issubset(uploaded_set):
        
        mapping = {}

        for col in expected:
            mapping[col] = {
                "type": "column",
                "source": col,
        }

        return df, mapping

    # ============================================
    # Continue with AI mapping
    # ============================================

    columns = list(df.columns)

    sample = df.head(5).to_markdown(index=False)

    prompt = f"""
        You are an expert business data engineer.

        A user uploaded a {dataset_type} CSV.

    Expected business schema:

        {expected}

        Uploaded columns:

        {columns}

        Sample data:

        {sample}

        Your task is to transform ANY business dataset into GemBiz's internal schema.

        For every expected field:

        1. If an uploaded column directly matches it,
           return:

        "type":"column"

        2. If it can be computed,
        return

        "type":"formula"

        Examples:

        Allowed formulas ONLY:

        Revenue = Price * Quantity

        Revenue = Unit Price * Units Sold

        Revenue = Amount

        Units Sold = Quantity

        Units Sold = Qty

        Minimum Stock = 20% of Stock

        Supplier = "Unknown"

        Category = "General"

        Use ONLY one of these formulas exactly as written.

        If none apply, return

        {{
            "type":"missing"
        }}

        Never invent new formulas.

        3. If no data exists but a reasonable business assumption can be made,
        return

        "type":"assumption"

        Examples:

        Minimum Stock = 20% of Stock

        Supplier = "Unknown"

        Category = "General"

        If nothing is possible,
        return

        "type":"missing"

        Return ONLY valid JSON.

        The JSON MUST contain one object for EVERY expected field.

        If a field cannot be mapped, return

        {{
            "type":"missing"
        }}

        Never omit an expected field.

        Example:

        {{
            "Revenue": {{
                "type": "formula",
                "formula": "Price * Quantity"
            }},

            "Product": {{
                "type": "column",
                "source": "SKU"
            }},

            "Minimum Stock": {{
                "type": "assumption",
                "value": "20% of Stock"
            }}
        }}
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

    try:
        mapping = json.loads(text)

    except Exception as e:

        print("Failed to parse Gemma response")
        print(e)
        print(text)

        return df, {}

    rename_dict = {}

    for expected_col, info in mapping.items():

        if not isinstance(info, dict):
            continue

        if info.get("type") == "column":

            source = info.get("source")

            if source in df.columns:

                rename_dict[source] = expected_col

    df.rename(
        columns=rename_dict,
        inplace=True,
    )

    return df,mapping