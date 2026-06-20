import re
import xml.etree.ElementTree as ET
from pathlib import Path

from app.models import CanonicalInvoice


def _local_name(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def _first_text_by_local_name(root: ET.Element, name: str) -> str:
    for elem in root.iter():
        if _local_name(elem.tag) == name and elem.text:
            return elem.text.strip()
    return ""


def _all_by_local_name(root: ET.Element, name: str) -> list[ET.Element]:
    return [elem for elem in root.iter() if _local_name(elem.tag) == name]


def parse_ubl_invoice(file_path: str) -> CanonicalInvoice:
    root = ET.parse(file_path).getroot()

    invoice_number = _first_text_by_local_name(root, "ID")
    issue_date = _first_text_by_local_name(root, "IssueDate")
    currency = _first_text_by_local_name(root, "DocumentCurrencyCode")
    payable_amount = _first_text_by_local_name(root, "PayableAmount")

    # UBL has multiple Name nodes. For the lab samples, the first one under
    # AccountingSupplierParty is supplier, and the first one under
    # AccountingCustomerParty is customer.
    supplier = ""
    customer = ""

    for elem in root.iter():
        if _local_name(elem.tag) == "AccountingSupplierParty":
            supplier = _first_text_by_local_name(elem, "Name")
        if _local_name(elem.tag) == "AccountingCustomerParty":
            customer = _first_text_by_local_name(elem, "Name")

    return CanonicalInvoice(
        document_type="UBL_INVOICE",
        invoice_number=invoice_number,
        issue_date=issue_date,
        currency=currency,
        supplier=supplier,
        customer=customer,
        total_amount=payable_amount,
        source_file=file_path,
    )


def parse_cxml_invoice(file_path: str) -> CanonicalInvoice:
    root = ET.parse(file_path).getroot()

    invoice_number = ""
    issue_date = ""
    currency = ""
    supplier = ""
    customer = ""
    total_amount = ""

    header = next((e for e in root.iter() if _local_name(e.tag) == "InvoiceDetailRequestHeader"), None)
    if header is not None:
        invoice_number = header.attrib.get("invoiceID", "")
        issue_date = header.attrib.get("invoiceDate", "")[:10]

    money_nodes = _all_by_local_name(root, "Money")
    if money_nodes:
        total_amount = money_nodes[-1].text.strip() if money_nodes[-1].text else ""
        currency = money_nodes[-1].attrib.get("currency", "")

    addresses = _all_by_local_name(root, "Name")
    if addresses:
        supplier = addresses[0].text.strip() if addresses[0].text else ""
    if len(addresses) > 1:
        customer = addresses[1].text.strip() if addresses[1].text else ""

    return CanonicalInvoice(
        document_type="CXML_INVOICE",
        invoice_number=invoice_number,
        issue_date=issue_date,
        currency=currency,
        supplier=supplier,
        customer=customer,
        total_amount=total_amount,
        source_file=file_path,
    )


def parse_sap_idoc_invoice(file_path: str) -> CanonicalInvoice:
    root = ET.parse(file_path).getroot()

    invoice_number = _first_text_by_local_name(root, "BELNR")
    issue_date = _first_text_by_local_name(root, "DATUM")
    currency = _first_text_by_local_name(root, "CURCY")
    total_amount = _first_text_by_local_name(root, "SUMME")

    supplier = ""
    customer = ""

    for segment in _all_by_local_name(root, "E1EDKA1"):
        role = _first_text_by_local_name(segment, "PARVW")
        name = _first_text_by_local_name(segment, "NAME1")
        if role == "LF":
            supplier = name
        elif role in {"AG", "RE", "WE"}:
            customer = name

    return CanonicalInvoice(
        document_type="SAP_IDOC_INVOICE",
        invoice_number=invoice_number,
        issue_date=issue_date,
        currency=currency,
        supplier=supplier,
        customer=customer,
        total_amount=total_amount,
        source_file=file_path,
    )


def parse_edifact_invoic(file_path: str) -> CanonicalInvoice:
    """
    Minimal EDIFACT INVOIC parser for lab/demo purposes.

    It supports the included sample and common segments:
    - BGM+380+INV-2026-003+9
    - DTM+137:20260620:102
    - NAD+SU+++Supplier Name
    - NAD+BY+++Buyer Name
    - CUX+2:EUR:4
    - MOA+77:1200.50
    """
    content = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    segments = [s.strip() for s in content.replace("\n", "").split("'") if s.strip()]

    invoice_number = ""
    issue_date = ""
    currency = ""
    supplier = ""
    customer = ""
    total_amount = ""

    for segment in segments:
        parts = segment.split("+")
        tag = parts[0]

        if tag == "BGM" and len(parts) > 2:
            invoice_number = parts[2]

        elif tag == "DTM" and len(parts) > 1:
            date_parts = parts[1].split(":")
            if len(date_parts) >= 2 and date_parts[0] == "137":
                raw = date_parts[1]
                if len(raw) == 8:
                    issue_date = f"{raw[0:4]}-{raw[4:6]}-{raw[6:8]}"

        elif tag == "CUX" and len(parts) > 1:
            cux_parts = parts[1].split(":")
            if len(cux_parts) >= 2:
                currency = cux_parts[1]

        elif tag == "NAD" and len(parts) > 4:
            role = parts[1]
            name = parts[4]
            if role in {"SU", "SE"}:
                supplier = name
            elif role in {"BY", "IV"}:
                customer = name

        elif tag == "MOA" and len(parts) > 1:
            moa_parts = parts[1].split(":")
            if moa_parts[0] == "77" and len(moa_parts) > 1:
                total_amount = moa_parts[1]

    return CanonicalInvoice(
        document_type="EDIFACT_INVOIC",
        invoice_number=invoice_number,
        issue_date=issue_date,
        currency=currency,
        supplier=supplier,
        customer=customer,
        total_amount=total_amount,
        source_file=file_path,
    )


def parse_x12_810(file_path: str) -> CanonicalInvoice:
    """
    Minimal ANSI X12 810 parser for lab/demo purposes.

    Supports a simple sample:
    BIG*20260620*INV-2026-005
    N1*SU*Supplier Inc
    N1*BY*Customer LLC
    CUR*BY*USD
    TDS*120050
    """
    content = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    content = re.sub(r"\s+", "", content)
    segments = [s for s in content.split("~") if s]

    invoice_number = ""
    issue_date = ""
    currency = ""
    supplier = ""
    customer = ""
    total_amount = ""

    for segment in segments:
        parts = segment.split("*")
        tag = parts[0]

        if tag == "BIG":
            if len(parts) > 1 and len(parts[1]) == 8:
                raw = parts[1]
                issue_date = f"{raw[0:4]}-{raw[4:6]}-{raw[6:8]}"
            if len(parts) > 2:
                invoice_number = parts[2]

        elif tag == "N1" and len(parts) > 2:
            if parts[1] == "SU":
                supplier = parts[2]
            elif parts[1] == "BY":
                customer = parts[2]

        elif tag == "CUR" and len(parts) > 2:
            currency = parts[2]

        elif tag == "TDS" and len(parts) > 1:
            # X12 TDS is usually cents.
            try:
                total_amount = f"{int(parts[1]) / 100:.2f}"
            except ValueError:
                total_amount = parts[1]

    return CanonicalInvoice(
        document_type="X12_810",
        invoice_number=invoice_number,
        issue_date=issue_date,
        currency=currency,
        supplier=supplier,
        customer=customer,
        total_amount=total_amount,
        source_file=file_path,
    )


def parse_invoice(file_path: str, document_type: str) -> CanonicalInvoice:
    parsers = {
        "UBL_INVOICE": parse_ubl_invoice,
        "CXML_INVOICE": parse_cxml_invoice,
        "EDIFACT_INVOIC": parse_edifact_invoic,
        "X12_810": parse_x12_810,
        "SAP_IDOC_INVOICE": parse_sap_idoc_invoice,
    }

    if document_type not in parsers:
        raise ValueError(f"Unsupported document type: {document_type}")

    return parsers[document_type](file_path)
