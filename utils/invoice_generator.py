import random
from io import BytesIO
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)


# ==========================================================
# Generate Random Invoice Number
# ==========================================================

def generate_invoice_number():

    return f"INV-{random.randint(100000, 999999)}"


# ==========================================================
# Calculate Unit Price
# ==========================================================

def calculate_unit_price(
    sales_df,
    product,
):

    try:

        df = sales_df[
            sales_df["Product"] == product
        ].copy()

        revenue = df["Revenue"].sum()

        units = df["Units Sold"].sum()

        if units == 0:
            return 0

        return revenue / units

    except Exception:

        return 0


# ==========================================================
# Generate Invoice PDF
# ==========================================================

def generate_invoice_pdf(
    invoice_number,
    customer_name,
    customer_phone,
    product,
    quantity,
    sales_df,
):

    unit_price = calculate_unit_price(
        sales_df,
        product,
    )

    total = unit_price * quantity

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = 1

    heading = styles["Heading2"]

    normal = styles["BodyText"]

    footer = styles["Italic"]

    story = []

    # ======================================================
    # Title
    # ======================================================

    story.append(
        Paragraph(
            "<font size='22'><b>GemBiz Invoice</b></font>",
            title,
        )
    )

    story.append(
        Paragraph(
            datetime.now().strftime(
                "Generated on %d %B %Y"
            ),
            normal,
        )
    )

    story.append(Spacer(1, 20))

    # ======================================================
    # Invoice Details
    # ======================================================

    story.append(
        Paragraph(
            "Invoice Details",
            heading,
        )
    )

    story.append(
        Paragraph(
            f"""
<b>Invoice Number</b><br/>
{invoice_number}<br/><br/>

<b>Date</b><br/>
{datetime.now().strftime("%d-%m-%Y")}
""",
            normal,
        )
    )

    story.append(Spacer(1, 20))

    # ======================================================
    # Customer Details
    # ======================================================

    story.append(
        Paragraph(
            "Customer Details",
            heading,
        )
    )

    story.append(
        Paragraph(
            f"""
<b>Name</b><br/>
{customer_name}<br/><br/>

<b>Phone Number</b><br/>
{customer_phone}
""",
            normal,
        )
    )

    story.append(Spacer(1, 20))

    # ======================================================
    # Product Details
    # ======================================================

    story.append(
        Paragraph(
            "Product Details",
            heading,
        )
    )

    story.append(
        Paragraph(
            f"""
<b>Product</b><br/>
{product}<br/><br/>

<b>Quantity</b><br/>
{quantity}<br/><br/>

<b>Unit Price</b><br/>
Rs. {unit_price:,.2f}<br/><br/>

<b>Total Amount</b><br/>
Rs. {total:,.2f}
""",
            normal,
        )
    )

    story.append(Spacer(1, 25))

    # ======================================================
    # Footer
    # ======================================================

    story.append(
        Paragraph(
            "<hr/>",
            normal,
        )
    )

    story.append(
        Paragraph(
            "<b>GemBiz</b>",
            footer,
        )
    )

    story.append(
        Paragraph(
            "AI-Powered Business Intelligence",
            footer,
        )
    )

    story.append(
        Paragraph(
            "Powered by Google Gemma",
            footer,
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer