import pandas as pd

from utils.schema_mapper import map_columns

def infer_missing_columns(df, schema, dataset_type):
    """
    Infer missing columns required by GemBiz.
    """

    if dataset_type == "sales":

        # Revenue
        if "Revenue" not in df.columns:
        
            rule = schema.get("Revenue", {})

            if rule.get("type") == "formula":
            
                formula = rule.get("formula")

                if formula == "Price * Quantity":
                
                    df["Revenue"] = (
                        df["Price"] *
                        df["Quantity"]
                    )

                elif formula == "Unit Price * Units Sold":
                
                    df["Revenue"] = (
                        df["Unit Price"] *
                        df["Units Sold"]
                    )

        # Units Sold
        if "Units Sold" not in df.columns:
        
            rule = schema.get("Units Sold", {})
        
            if rule.get("type") == "formula":
            
                formula = rule.get("formula")
        
                if formula == "Quantity":
                
                    df["Units Sold"] = df["Quantity"]
        
                elif formula == "Qty":
                
                    df["Units Sold"] = df["Qty"]
        
            elif "Quantity" in df.columns:
            
                df["Units Sold"] = df["Quantity"]
        
            elif "Qty" in df.columns:
            
                df["Units Sold"] = df["Qty"]
        
            else:
            
                df["Units Sold"] = 1
        
    # -------------------------------------------------

    elif dataset_type == "inventory":

        if "Minimum Stock" not in df.columns:

            if "Stock" in df.columns:

                df["Minimum Stock"] = (
                    df["Stock"] * 0.20
                ).round().clip(lower=5)

            else:

                df["Minimum Stock"] = 5

        if "Supplier" not in df.columns:

            df["Supplier"] = "Unknown"

    # -------------------------------------------------

    elif dataset_type == "expenses":

        if "Category" not in df.columns:

            df["Category"] = "General"

    return df


def validate_schema(df, dataset_type):

    required = {

        "sales": [
            "Product",
            "Revenue",
            "Units Sold",
        ],

        "inventory": [
            "Product",
            "Stock",
            "Minimum Stock",
        ],

        "expenses": [
            "Category",
            "Amount",
        ],
    }

    missing = [

        col

        for col in required[dataset_type]

        if col not in df.columns

    ]

    if missing:

        raise ValueError(
            f"Unable to identify required columns: {missing}"
        )


def load_csv(file, dataset_type):

    if file is None:
        return None

    try:

        df = pd.read_csv(
            file,
            low_memory=False,
        )

        df, schema = map_columns(
            df,
            dataset_type,
        )

        df = infer_missing_columns(
            df,
            schema,
            dataset_type,
        )

        validate_schema(
            df,
            dataset_type,
        )

        return df

    except Exception as e:

        raise ValueError(
            f"Error processing {dataset_type} CSV:\n{e}"
        )