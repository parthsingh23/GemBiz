import plotly.express as px


def revenue_chart(sales_df):

    fig = px.line(
        sales_df,
        x="Date",
        y="Revenue",
        markers=True,
        title="Revenue Over Time"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig


def inventory_chart(inventory_df):

    fig = px.bar(
        inventory_df,
        x="Product",
        y="Stock",
        color="Stock",
        title="Inventory Status"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig


def expense_chart(expenses_df):

    fig = px.pie(
        expenses_df,
        names="Category",
        values="Amount",
        hole=0.45,
        title="Expense Breakdown"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400
    )

    return fig


def top_products_chart(sales_df):

    grouped = (
        sales_df
        .groupby("Product")["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        grouped,
        x="Product",
        y="Revenue",
        color="Revenue",
        title="Top Selling Products"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400
    )

    return fig