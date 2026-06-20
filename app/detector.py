from pathlib import Path


SUPPORTED_TYPES = {
    "UBL_INVOICE",
    "CXML_INVOICE",
    "EDIFACT_INVOIC",
    "X12_810",
    "SAP_IDOC_INVOICE",
    "UNKNOWN",
}


def detect_document_type(file_path: str) -> str:
    """
    Detect document type by inspecting payload markers.

    This intentionally mirrors a common B2B middleware approach:
    look at namespace, root node, EDI transaction marker, or IDoc segment.
    """
    content = Path(file_path).read_text(encoding="utf-8", errors="ignore").strip()

    if "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" in content or "<Invoice" in content:
        return "UBL_INVOICE"

    if "<cXML" in content or "<InvoiceDetailRequest" in content:
        return "CXML_INVOICE"

    if content.startswith("UNB") or ("UNH" in content and "INVOIC" in content):
        return "EDIFACT_INVOIC"

    if content.startswith("ISA") or "ST*810" in content:
        return "X12_810"

    if "<IDOC" in content or "<E1EDK01" in content or "<EDI_DC40" in content:
        return "SAP_IDOC_INVOICE"

    return "UNKNOWN"
