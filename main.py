import argparse
import json
from pathlib import Path

from app.pipeline import process_invoice


def main() -> None:
    parser = argparse.ArgumentParser(description="SAP B2B Invoice Integration Lab")
    parser.add_argument(
        "file",
        nargs="?",
        default="input/invoice_ubl.xml",
        help="Path to invoice file. Default: input/invoice_ubl.xml",
    )
    args = parser.parse_args()

    if not Path(args.file).exists():
        raise FileNotFoundError(f"Input file not found: {args.file}")

    report = process_invoice(args.file)

    print("\n=== SAP B2B Invoice Integration Lab ===")
    print(f"Source file: {report.source_file}")
    print(f"Document type: {report.document_type}")
    print(f"Invoice number: {report.invoice_number}")
    print(f"Status: {report.status}")

    if report.errors:
        print("\nErrors:")
        for error in report.errors:
            print(f"- {error}")

    if report.route:
        print("\nRoute:")
        print(json.dumps(report.route, indent=2))

    print("\nOutput files:")
    for file in report.output_files:
        print(f"- {file}")


if __name__ == "__main__":
    main()
