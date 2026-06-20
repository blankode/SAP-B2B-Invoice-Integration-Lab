from pathlib import Path

from app.models import RouteDecision


def simulate_transport(payload: str, route: RouteDecision, invoice_number: str) -> str:
    """
    Simulates a technical send step.

    No real network calls are made. The payload is written into an output folder
    named after the selected receiver/protocol.
    """
    safe_invoice = invoice_number.replace("/", "_").replace("\\", "_") or "unknown_invoice"

    target_folder = Path("output") / route.receiver / route.protocol
    target_folder.mkdir(parents=True, exist_ok=True)

    if route.protocol == "NONE":
        file_path = target_folder / f"{safe_invoice}_manual_review.txt"
    elif route.protocol == "AS2":
        file_path = target_folder / f"{safe_invoice}_as2_payload.xml"
    elif route.protocol == "SFTP":
        file_path = target_folder / f"{safe_invoice}_sftp_payload.xml"
    elif route.protocol == "HTTPS":
        file_path = target_folder / f"{safe_invoice}_https_payload.xml"
    else:
        file_path = target_folder / f"{safe_invoice}_payload.xml"

    file_path.write_text(payload, encoding="utf-8")
    return str(file_path)
