from app.pipeline import process_invoice


def test_process_ubl_success():
    report = process_invoice("input/invoice_ubl.xml")
    assert report.status == "SUCCESS"
    assert report.document_type == "UBL_INVOICE"
    assert report.invoice_number == "INV-2026-001"


def test_process_invalid_invoice_fails():
    report = process_invoice("input/invoice_ubl_invalid_missing_amount.xml")
    assert report.status == "FAILED"
    assert any("total_amount" in error for error in report.errors)
