import plotly.express as px
import plotly.graph_objects as go


def revenue_chart(df):

    revenue = (
        df.groupby("Date")["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        revenue,
        x="Date",
        y="Revenue",
        title="Revenue Trend"
    )

    return fig


def expense_chart(df):

    expense = (
        df.groupby("Category")["Amount"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        expense,
        x="Category",
        y="Amount",
        title="Expenses"
    )

    return fig


def inventory_chart(df):

    fig = px.bar(
        df,
        x="Product",
        y="Stock",
        title="Inventory"
    )

    return fig


def top_products_chart(df):

    top = (
        df.groupby("Product")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(
            "Revenue",
            ascending=False
        )
    )

    fig = px.bar(
        top,
        x="Product",
        y="Revenue",
        title="Top Selling Products"
    )

    return fig


def forecast_chart(history_df, forecast_df):

    fig = go.Figure()

    historical = (
        history_df.groupby("Date")["Revenue"]
        .sum()
        .reset_index()
    )

    fig.add_trace(
        go.Scatter(
            x=historical["Date"],
            y=historical["Revenue"],
            mode="lines+markers",
            name="Historical"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_df["Date"],
            y=forecast_df["Predicted Revenue"],
            mode="lines+markers",
            name="Forecast"
        )
    )

    fig.update_layout(
        title="7-Day Revenue Forecast"
    )

    return fig