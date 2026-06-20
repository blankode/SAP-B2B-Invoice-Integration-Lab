import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

from app.models import CanonicalInvoice


def to_canonical_json(invoice: CanonicalInvoice) -> str:
    return json.dumps(invoice.to_dict(), indent=2, ensure_ascii=False)


def map_to_sap_idoc(invoice: CanonicalInvoice) -> str:
    """
    Map canonical invoice to an IDoc-like INVOIC02 XML.

    This is not meant to be a complete SAP IDoc implementation.
    It is a portfolio-friendly representation of the mapping concept.
    """
    idoc = ET.Element("IDOC", {"BEGIN": "1"})

    control = ET.SubElement(idoc, "EDI_DC40", {"SEGMENT": "1"})
    ET.SubElement(control, "TABNAM").text = "EDI_DC40"
    ET.SubElement(control, "IDOCTYP").text = "INVOIC02"
    ET.SubElement(control, "MESTYP").text = "INVOIC"
    ET.SubElement(control, "SNDPOR").text = "B2B_LAB"
    ET.SubElement(control, "RCVPOR").text = "SAP_ERP"

    header = ET.SubElement(idoc, "E1EDK01", {"SEGMENT": "1"})
    ET.SubElement(header, "BELNR").text = invoice.invoice_number
    ET.SubElement(header, "CURCY").text = invoice.currency
    ET.SubElement(header, "DATUM").text = invoice.issue_date

    supplier = ET.SubElement(idoc, "E1EDKA1", {"SEGMENT": "1"})
    ET.SubElement(supplier, "PARVW").text = "LF"
    ET.SubElement(supplier, "NAME1").text = invoice.supplier

    customer = ET.SubElement(idoc, "E1EDKA1", {"SEGMENT": "1"})
    ET.SubElement(customer, "PARVW").text = "AG"
    ET.SubElement(customer, "NAME1").text = invoice.customer

    total = ET.SubElement(idoc, "E1EDS01", {"SEGMENT": "1"})
    ET.SubElement(total, "SUMID").text = "010"
    ET.SubElement(total, "SUMME").text = invoice.total_amount

    rough_string = ET.tostring(idoc, encoding="utf-8")
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent="  ")


def map_to_sap_proxy_payload(invoice: CanonicalInvoice) -> str:
    root = ET.Element("InvoiceCreateRequest")
    ET.SubElement(root, "InvoiceNumber").text = invoice.invoice_number
    ET.SubElement(root, "IssueDate").text = invoice.issue_date
    ET.SubElement(root, "Currency").text = invoice.currency
    ET.SubElement(root, "SupplierName").text = invoice.supplier
    ET.SubElement(root, "CustomerName").text = invoice.customer
    ET.SubElement(root, "GrossAmount").text = invoice.total_amount

    rough_string = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent="  ")
