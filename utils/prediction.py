import pandas as pd
import numpy as np


def forecast_sales(sales_df, days=7):
    """
    Forecast future revenue using a simple linear trend.
    """

    if sales_df is None or len(sales_df) < 2:
        return None

    df = sales_df.copy()

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    daily_sales = (
        df.groupby("Date")["Revenue"]
        .sum()
        .reset_index()
    )

    x = np.arange(len(daily_sales))
    y = daily_sales["Revenue"].values

    slope, intercept = np.polyfit(x, y, 1)

    future_x = np.arange(len(daily_sales), len(daily_sales) + days)

    predictions = intercept + slope * future_x

    predictions = np.maximum(predictions, 0)

    future_dates = pd.date_range(
        start=daily_sales["Date"].max() + pd.Timedelta(days=1),
        periods=days
    )

    forecast_df = pd.DataFrame(
        {
            "Date": future_dates,
            "Predicted Revenue": predictions
        }
    )

    return forecast_df