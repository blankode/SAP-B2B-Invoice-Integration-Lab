# Interview Explanation

## 30-second version

I built a SAP B2B Invoice Integration Lab that simulates a production-style invoice integration flow. It detects input formats like UBL, cXML, EDIFACT, X12 and IDoc, converts them into a canonical invoice model, validates mandatory fields, maps the result into SAP IDoc-like XML, applies routing rules, simulates transport and generates a processing report.

## 2-minute version

The project is meant to show practical integration thinking, not just Python scripting.

The flow starts with document detection. The system inspects the incoming payload and decides whether it is UBL, cXML, EDIFACT, X12 or an IDoc-like XML. Then a parser extracts the relevant business fields and normalizes them into a canonical invoice model.

After that, the validation layer checks mandatory data such as invoice number, issue date, currency, supplier, customer and total amount. If the payload is invalid, the system creates a failed processing report. If it is valid, the mapping layer generates a SAP IDoc-like XML and a SAP proxy-like payload.

The routing engine then chooses the receiver and protocol based on business rules. For example, a Romanian customer is routed to a simulated SAP ERP Romania receiver via SFTP, while a German partner can be routed via AS2.

The final step simulates transport and generates a monitoring report that contains status, errors, receiver, protocol and generated files.

## What this demonstrates

- Payload detection
- Multi-format parsing
- Canonical data model design
- Mandatory field validation
- Mapping into SAP-style structures
- Partner-specific routing
- Error handling
- Monitoring/reporting
- B2B/SAP integration thinking

## How to position it in interviews

Do not say:

> I built a Python invoice parser.

Say:

> I built a middleware-style B2B invoice processing lab. It simulates the same integration lifecycle used in SAP CPI, PI/PO or B2B gateways: document detection, mapping, validation, routing, transport and monitoring.

## Possible interview questions

### How do you troubleshoot a failed invoice?

I first separate the problem into connectivity, protocol, payload, mapping, validation and receiver-system issues. I check whether the message was received, whether the document type was correctly detected, whether mandatory fields are present, whether mapping generated the expected target structure and whether the receiver route was selected correctly.

### Why use a canonical model?

A canonical model prevents every source format from needing a direct mapping to every target format. UBL, cXML, EDIFACT, X12 and IDoc can all be normalized into one internal invoice structure, and target mappings can be built from there.

### What would you improve next?

I would add real AS2/SFTP connectivity, persistence in a database, more detailed EDIFACT/X12 parsing, partner configuration files, retry handling, message correlation IDs and a more complete dashboard.
