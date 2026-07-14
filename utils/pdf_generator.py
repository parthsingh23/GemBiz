from io import BytesIO
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)


def generate_pdf(kpis, report, forecast_df):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("<b>GemBiz Business Report</b>", styles["Title"])
    )

    story.append(
        Paragraph(
            datetime.now().strftime(
                "Generated on %d %B %Y, %I:%M %p"
            ),
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph("<b>Business KPIs</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            f"""
Revenue : ₹{kpis['Revenue']:,.0f}<br/>
Expenses : ₹{kpis['Expenses']:,.0f}<br/>
Profit : ₹{kpis['Profit']:,.0f}<br/>
Inventory : {kpis['Inventory']} Units<br/>
Health Score : {kpis['Health Score']}/100
""",
            styles["BodyText"],
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph("<b>AI Business Report</b>", styles["Heading2"])
    )

    report = report.replace("\n", "<br/>")

    story.append(
        Paragraph(report, styles["BodyText"])
    )

    story.append(Spacer(1, 15))

    if forecast_df is not None:

        story.append(
            Paragraph(
                "<b>Revenue Forecast</b>",
                styles["Heading2"],
            )
        )

        avg = forecast_df["Predicted Revenue"].mean()

        trend = (
            "Increasing"
            if forecast_df.iloc[-1]["Predicted Revenue"]
            >
            forecast_df.iloc[0]["Predicted Revenue"]
            else "Decreasing"
        )

        story.append(
            Paragraph(
                f"""
Expected Average Revenue:
₹{avg:,.0f}<br/><br/>

Business Trend:
{trend}
""",
                styles["BodyText"],
            )
        )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Generated using GemBiz • Powered by Google Gemma",
            styles["Italic"],
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer