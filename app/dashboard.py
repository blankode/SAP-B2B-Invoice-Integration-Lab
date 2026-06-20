import json
from pathlib import Path

import streamlit as st


st.set_page_config(page_title="SAP B2B Invoice Integration Lab", layout="wide")

st.title("SAP B2B Invoice Integration Lab")
st.caption("B2B invoice processing simulator: detection, validation, mapping, routing and monitoring.")

report_path = Path("output/processing_report.json")
canonical_path = Path("output/canonical_invoice.json")
idoc_path = Path("output/sap_idoc_invoice.xml")
proxy_path = Path("output/sap_proxy_invoice.xml")

if not report_path.exists():
    st.warning("No processing report found. Run `python main.py input/invoice_ubl.xml` first.")
    st.stop()

report = json.loads(report_path.read_text(encoding="utf-8"))

col1, col2, col3, col4 = st.columns(4)
col1.metric("Status", report.get("status", "UNKNOWN"))
col2.metric("Document Type", report.get("document_type", ""))
col3.metric("Invoice", report.get("invoice_number", ""))
col4.metric("Receiver", report.get("route", {}).get("receiver", ""))

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Processing Report")
    st.json(report)

    st.subheader("Canonical Invoice")
    if canonical_path.exists():
        st.json(json.loads(canonical_path.read_text(encoding="utf-8")))
    else:
        st.info("Canonical invoice not generated.")

with right:
    st.subheader("Route")
    st.json(report.get("route", {}))

    st.subheader("Errors")
    errors = report.get("errors", [])
    if errors:
        st.error("\n".join(errors))
    else:
        st.success("No validation or processing errors.")

    st.subheader("SAP IDoc-like Output")
    if idoc_path.exists():
        st.code(idoc_path.read_text(encoding="utf-8"), language="xml")
    else:
        st.info("SAP IDoc-like output not generated.")

    st.subheader("SAP Proxy-like Output")
    if proxy_path.exists():
        st.code(proxy_path.read_text(encoding="utf-8"), language="xml")
    else:
        st.info("SAP Proxy-like output not generated.")
