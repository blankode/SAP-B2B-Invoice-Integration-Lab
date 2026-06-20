# SAP B2B Invoice Integration Lab

A portfolio project that simulates a B2B invoice integration flow between external partners and a SAP ERP receiver.

The goal is to demonstrate production-like integration thinking: document detection, parsing, validation, canonical mapping, SAP IDoc-like transformation, routing, simulated transport, monitoring and error reporting.

## Why this project exists

This project is designed for SAP CPI / SAP PI/PO / B2B Integration Consultant interviews.

It shows that you understand the core integration lifecycle:

```text
Partner System
    -> B2B Middleware
    -> Document Detection
    -> Parsing
    -> Business Validation
    -> Canonical Model
    -> Mapping
    -> Routing
    -> SAP Receiver
    -> Monitoring Report
```

## Supported input types

- UBL Invoice XML
- cXML Invoice
- EDIFACT INVOIC
- ANSI X12 810
- SAP IDoc-like XML

## Generated output

- Canonical invoice JSON
- SAP IDoc-like XML
- SAP proxy-like XML
- Processing report JSON
- Simulated receiver payload under `output/<receiver>/<protocol>/`

## Project structure

```text
sap-b2b-invoice-integration-lab/
├── app/
│   ├── detector.py
│   ├── parsers.py
│   ├── validator.py
│   ├── mapper.py
│   ├── router.py
│   ├── transport_simulator.py
│   ├── pipeline.py
│   ├── logger.py
│   ├── models.py
│   └── dashboard.py
├── input/
│   ├── invoice_ubl.xml
│   ├── invoice_ubl_invalid_missing_amount.xml
│   ├── invoice_cxml.xml
│   ├── invoice_edifact.txt
│   ├── invoice_x12_810.txt
│   └── invoice_idoc.xml
├── output/
├── docs/
├── tests/
├── scripts/
├── main.py
└── requirements.txt
```

## Quick start

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the default UBL invoice:

```bash
python main.py
```

Run a specific input:

```bash
python main.py input/invoice_cxml.xml
python main.py input/invoice_edifact.txt
python main.py input/invoice_x12_810.txt
python main.py input/invoice_idoc.xml
python main.py input/invoice_ubl_invalid_missing_amount.xml
```

Run all sample files:

```bash
python scripts/run_all_samples.py
```

Run the dashboard:

```bash
streamlit run app/dashboard.py
```

Run tests:

```bash
pytest
```

## Example successful output

```text
=== SAP B2B Invoice Integration Lab ===
Source file: input/invoice_ubl.xml
Document type: UBL_INVOICE
Invoice number: INV-2026-001
Status: SUCCESS

Route:
{
  "receiver": "SAP_ERP_RO",
  "protocol": "SFTP",
  "target_path": "/sap/ro/inbound/invoice/",
  "as2_partner_id": "",
  "reason": "Romanian customer routing rule"
}
```

## Interview explanation

I built a SAP B2B Invoice Integration Lab to simulate how external partner invoices are processed before reaching SAP. The flow detects the document type, parses the payload, validates mandatory fields, maps the data into a canonical invoice model, transforms it into a SAP IDoc-like XML structure, applies partner-specific routing rules, simulates transport, and generates processing reports.

The value of the project is not only the parser. The value is the full integration flow: validation, mapping, routing, error handling and monitoring.
