from pathlib import Path

from app.pipeline import process_invoice


samples = [
    "input/invoice_ubl.xml",
    "input/invoice_cxml.xml",
    "input/invoice_edifact.txt",
    "input/invoice_x12_810.txt",
    "input/invoice_idoc.xml",
    "input/invoice_ubl_invalid_missing_amount.xml",
]

for sample in samples:
    print("\n" + "=" * 80)
    print(f"Processing {sample}")
    report = process_invoice(sample)
    print(f"Status: {report.status}")
    print(f"Document type: {report.document_type}")
    print(f"Invoice: {report.invoice_number}")
    if report.errors:
        print("Errors:")
        for error in report.errors:
            print(f"- {error}")
