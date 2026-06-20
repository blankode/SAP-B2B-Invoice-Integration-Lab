from app.detector import detect_document_type


def test_detect_ubl():
    assert detect_document_type("input/invoice_ubl.xml") == "UBL_INVOICE"


def test_detect_cxml():
    assert detect_document_type("input/invoice_cxml.xml") == "CXML_INVOICE"


def test_detect_edifact():
    assert detect_document_type("input/invoice_edifact.txt") == "EDIFACT_INVOIC"


def test_detect_x12():
    assert detect_document_type("input/invoice_x12_810.txt") == "X12_810"


def test_detect_idoc():
    assert detect_document_type("input/invoice_idoc.xml") == "SAP_IDOC_INVOICE"
