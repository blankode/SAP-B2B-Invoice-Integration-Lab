from pathlib import Path

from app.detector import detect_document_type
from app.logger import write_json_file, write_processing_report, write_text_file
from app.mapper import map_to_sap_idoc, map_to_sap_proxy_payload
from app.models import CanonicalInvoice, ProcessingReport
from app.parsers import parse_invoice
from app.router import route_invoice
from app.transport_simulator import simulate_transport
from app.validator import validate_invoice


def process_invoice(file_path: str) -> ProcessingReport:
    Path("output").mkdir(exist_ok=True)

    output_files: list[str] = []
    errors: list[str] = []
    invoice: CanonicalInvoice | None = None
    route = None

    document_type = detect_document_type(file_path)

    try:
        if document_type == "UNKNOWN":
            raise ValueError("Unknown or unsupported document type")

        invoice = parse_invoice(file_path, document_type)
        validation_errors = validate_invoice(invoice)
        errors.extend(validation_errors)

        if invoice:
            canonical_file = write_json_file("output/canonical_invoice.json", invoice.to_dict())
            output_files.append(canonical_file)

        route = route_invoice(invoice)

        if not errors:
            idoc_payload = map_to_sap_idoc(invoice)
            proxy_payload = map_to_sap_proxy_payload(invoice)

            idoc_file = write_text_file("output/sap_idoc_invoice.xml", idoc_payload)
            proxy_file = write_text_file("output/sap_proxy_invoice.xml", proxy_payload)

            output_files.extend([idoc_file, proxy_file])

            transport_file = simulate_transport(idoc_payload, route, invoice.invoice_number)
            output_files.append(transport_file)

    except Exception as exc:
        errors.append(str(exc))

    report = ProcessingReport.build(
        source_file=file_path,
        invoice=invoice,
        document_type=document_type,
        errors=errors,
        route=route,
        output_files=output_files,
    )

    report_file = write_processing_report(report)
    report.output_files.append(report_file)
    write_processing_report(report)

    return report
