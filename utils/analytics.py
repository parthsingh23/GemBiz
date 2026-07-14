import pandas as pd


def calculate_kpis(sales_df, inventory_df, expenses_df):

    revenue = 0
    expenses = 0
    profit = 0
    inventory = 0
    health = 0

    if sales_df is not None:
        revenue = sales_df["Revenue"].sum()

    if expenses_df is not None:
        expenses = expenses_df["Amount"].sum()

    if inventory_df is not None:
        inventory = inventory_df["Stock"].sum()

    profit = revenue - expenses

    # -----------------------------
    # Business Health Score
    # -----------------------------

    score = 100

    if revenue > 0:

        expense_ratio = expenses / revenue

        if expense_ratio > 0.80:
            score -= 30

        elif expense_ratio > 0.60:
            score -= 15

    if profit < 0:
        score -= 30

    elif profit < revenue * 0.15:
        score -= 10

    if inventory_df is not None:

        low_stock = (
            inventory_df["Stock"]
            <
            inventory_df["Minimum Stock"]
        ).sum()

        score -= low_stock * 5

    score = max(0, min(score, 100))

    if score >= 85:
        status = "Excellent 🟢"

    elif score >= 70:
        status = "Good 🟡"

    elif score >= 50:
        status = "Average 🟠"

    else:
        status = "Poor 🔴"

    return {

        "Revenue": revenue,

        "Expenses": expenses,

        "Profit": profit,

        "Inventory": inventory,

        "Health Score": score,

        "Health Status": status

    }