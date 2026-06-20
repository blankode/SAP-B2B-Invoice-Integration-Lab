from datetime import datetime

from app.models import CanonicalInvoice


def validate_invoice(invoice: CanonicalInvoice) -> list[str]:
    errors: list[str] = []

    required_fields = [
        "invoice_number",
        "issue_date",
        "currency",
        "supplier",
        "customer",
        "total_amount",
    ]

    data = invoice.to_dict()

    for field in required_fields:
        if not str(data.get(field, "")).strip():
            errors.append(f"Missing mandatory field: {field}")

    if invoice.issue_date:
        try:
            datetime.strptime(invoice.issue_date, "%Y-%m-%d")
        except ValueError:
            errors.append("Issue date must use YYYY-MM-DD format")

    if invoice.currency and len(invoice.currency) != 3:
        errors.append("Currency must be a 3-letter code, example: EUR")

    if invoice.total_amount:
        try:
            amount = float(invoice.total_amount)
            if amount <= 0:
                errors.append("Total amount must be greater than zero")
        except ValueError:
            errors.append("Total amount is not a valid number")

    return errors
