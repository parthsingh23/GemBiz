from io import BytesIO
from datetime import datetime
import re

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)


def clean_ai_report(report):

    if report is None:
        return "AI report unavailable."

    report = str(report)

    # Remove code fences
    report = report.replace("```", "")

    # Remove markdown
    report = report.replace("**", "")
    report = report.replace("__", "")
    report = report.replace("#", "")

    # Remove common AI title
    report = re.sub(
        r"business analysis report",
        "",
        report,
        flags=re.IGNORECASE,
    )

    # Remove numbered headings
    report = re.sub(
        r"(?m)^\s*\d+\.\s*",
        "",
        report,
    )

    # Convert bullets
    report = re.sub(
        r"(?m)^\*\s+",
        "• ",
        report,
    )

    report = re.sub(
        r"(?m)^-\s+",
        "• ",
        report,
    )

    # Remove excessive blank lines
    report = re.sub(
        r"\n{3,}",
        "\n\n",
        report,
    )

    return report.strip()


def generate_pdf(kpis, report, forecast_df):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = 1

    heading_style = styles["Heading2"]
    heading_style.spaceAfter = 10
    heading_style.spaceBefore = 10

    normal_style = styles["BodyText"]
    footer_style = styles["Italic"]

    story = []

    # ======================================================
    # Title
    # ======================================================

    story.append(
        Paragraph(
            "<font size='24'><b>GemBiz AI Business Intelligence Report</b></font>",
            title_style,
        )
    )

    story.append(
        Paragraph(
            datetime.now().strftime(
                "Generated on %d %B %Y, %I:%M %p"
            ),
            normal_style,
        )
    )

    story.append(Spacer(1, 20))

    # ======================================================
    # KPIs
    # ======================================================

    story.append(
        Paragraph(
            "Business Overview",
            heading_style,
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            f"""
            <b>Revenue</b> : Rs. {kpis['Revenue']:,.0f}<br/><br/>

            <b>Expenses</b> : Rs. {kpis['Expenses']:,.0f}<br/><br/>

            <b>Profit</b> : Rs. {kpis['Profit']:,.0f}<br/><br/>

            <b>Inventory</b> : {kpis['Inventory']} Units<br/><br/>

            <b>Health Score</b> : {kpis['Health Score']}/100
        """,
            normal_style,
        )
    )

    story.append(Spacer(1, 20))

    # ======================================================
    # AI Report
    # ======================================================

    story.append(
        Paragraph(
            "AI Business Report",
            heading_style,
        )
    )

    story.append(Spacer(1, 10))

    report = clean_ai_report(report)

    headings = [
        "Business Summary",
        "Strengths",
        "Weaknesses",
        "Risks",
        "Actionable Recommendations",
    ]

    for line in report.splitlines():

        line = line.strip()

        if not line:
            story.append(Spacer(1, 8))
            continue

        if line in headings:

            story.append(
                Paragraph(
                    f"<b>{line}</b>",
                    heading_style,
                )
            )

            story.append(Spacer(1, 6))

        else:

            story.append(
                Paragraph(
                    line,
                    normal_style,
                )
            )

    story.append(Spacer(1, 20))

    # ======================================================
    # Forecast
    # ======================================================

    if forecast_df is not None and not forecast_df.empty:

        story.append(
            Paragraph(
                "Revenue Forecast",
                heading_style,
            )
        )

        story.append(Spacer(1, 8))

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
                <b>Predicted Average Revenue</b> :
                Rs. {avg:,.0f}<br/><br/>

                <b>Business Trend</b> :
                {trend}
            """,
                normal_style,
            )
        )

    story.append(Spacer(1, 30))

    # ======================================================
    # Footer
    # ======================================================

    story.append(
    Paragraph(
        "<br/><hr/>",
        normal_style,
        )
    )

    story.append(Spacer(1,10))

    story.append(
    Paragraph(
        "<b>GemBiz</b>",
        footer_style,
        )
    )
    
    story.append(
        Paragraph(
            "AI-Powered Business Intelligence Platform",
            footer_style,
        )
    )
    
    story.append(
        Paragraph(
            datetime.now().strftime(
                "Generated on %d %B %Y"
            ),
            footer_style,
        )
    )
    
    story.append(
        Paragraph(
            "Powered by Google Gemma",
            footer_style,
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer