def calculate_kpis(sales_df, inventory_df, expenses_df):

    revenue = 0
    expenses = 0
    profit = 0
    inventory = 0

    if sales_df is not None:
        revenue = sales_df["Revenue"].sum()

    if expenses_df is not None:
        expenses = expenses_df["Amount"].sum()

    if inventory_df is not None:
        inventory = inventory_df["Stock"].sum()

    profit = revenue - expenses

    return {
        "Revenue": revenue,
        "Expenses": expenses,
        "Profit": profit,
        "Inventory": inventory
    }