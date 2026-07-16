import random
from io import BytesIO
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.units import inch


# ==========================================================
# Generate Random Invoice Number
# ==========================================================

def generate_invoice_number():
    # Adjusted to match the 9-digit format in the GEMBIZ FORMAT reference
    return f"INV-{random.randint(100000,999999)}"


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
    products,
    quantities,
    sales_df,
):
    table_data = [
        ["S NO.", "ITEM", "QUANTITY", "RATE", "TOTAL"]
    ]

    grand_total = 0

    for i, product in enumerate(products, start=1):

        qty = quantities[product]

        unit_price = calculate_unit_price(
            sales_df,
            product,
        )

        line_total = qty * unit_price

        grand_total += line_total

        table_data.append([
            str(i),
            product,
            str(qty),
            f"Rs. {unit_price:,.2f}",
            f"Rs. {line_total:,.2f}",
        ])

    # Business Logic matching GEMBIZ FORMAT.xlsx
    discount_rate = 0.02
    discount_amount = grand_total * discount_rate

    subtotal_after_discount = (
        grand_total - discount_amount
    )

    gst_rate = 0.18
    gst_amount = subtotal_after_discount * gst_rate
    net_payable = subtotal_after_discount + gst_amount

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
    heading.alignment = 1

    normal = styles["BodyText"]

    story = []

    story.append(
        Paragraph(
            "<font size='24'><b>GEMBIZ</b></font>",
            title,
        )
    )

    story.append(
        Paragraph(
            "<b>AI Business Intelligence Platform</b>",
            normal,
        )
    )

    story.append(
        Paragraph(
            "<font size='16'><b>TAX INVOICE</b></font>",
            heading,
        )
    )

    story.append(Spacer(1, 15))

    # ======================================================
    # Header Details
    # ======================================================

    header_table = Table(
        [[
            Paragraph(
                f"""
                <b>Buyer</b><br/>
                {customer_name}<br/>
                <b>Phone</b><br/>
                {customer_phone}
                """,
                normal,
            ),

            Paragraph(
                f"""
                <b>Invoice No.</b><br/>
                {invoice_number}<br/>
                <b>Date</b><br/>
                {datetime.now().strftime("%d-%m-%Y")}
                """,
                normal,
            ),
        ]],
        colWidths=[260, 220],
    )

    header_table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),1,colors.black),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),8),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))

    story.append(header_table)
    story.append(Spacer(1, 15))

    # ======================================================
    # Product Table & Calculations
    # ======================================================

    table_data.extend([

        [
            "TOTAL",
            "",
            "",
            "",
            f"Rs. {grand_total:,.2f}",
        ],

        [
            "DISCOUNT (2%)",
            "",
            "",
            "",
            f"- Rs. {discount_amount:,.2f}",
        ],

        [
            "GST (18%)",
            "",
            "",
            "",
            f"Rs. {gst_amount:,.2f}",
        ],

        [
            "NET PAYABLE",
            "",
            "",
            "",
            f"Rs. {net_payable:,.2f}",
        ],
    ])

    summary_start = len(products) + 1
    
    # Configure table dimensions
    t = Table(table_data, colWidths=[1.2*inch, 2*inch, 1*inch, 1*inch, 1.2*inch])

    t.setStyle(TableStyle([
        # Header formatting
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (1,1), (1,len(products)), 'LEFT'),
        ('ALIGN', (4,1), (4,-1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),

        # Structure borders
        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        # Row Spans for Summaries
        ('SPAN', (0, summary_start), (3, summary_start)),

        ('SPAN', (0, summary_start + 1), (3, summary_start + 1)),

        ('SPAN', (0, summary_start + 2), (3, summary_start + 2)),

        ('SPAN', (0, summary_start + 3), (3, summary_start + 3)),

        # Summary Bold Fonts
        ('FONTNAME', (0, summary_start), (-1, -1), 'Helvetica-Bold'),

        # Padding
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))

    story.append(t)
    story.append(Spacer(1, 30))

    # ======================================================
    # Footer
    # ======================================================

    footer_text = f"""
    <hr/>

    <b>Generated using GemBiz</b><br/>

    Powered by Google Gemma<br/><br/>

    This invoice was generated electronically.<br/>

    No signature required.
    """

    story.append(Paragraph(footer_text, normal))

    doc.build(story)
    buffer.seek(0)

    return buffer