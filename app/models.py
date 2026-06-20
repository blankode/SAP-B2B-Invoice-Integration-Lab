from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any


@dataclass
class CanonicalInvoice:
    document_type: str
    invoice_number: str
    issue_date: str
    currency: str
    supplier: str
    customer: str
    total_amount: str
    source_file: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RouteDecision:
    receiver: str
    protocol: str
    target_path: str = ""
    as2_partner_id: str = ""
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProcessingReport:
    timestamp: str
    source_file: str
    invoice_number: str
    document_type: str
    status: str
    errors: list[str]
    route: dict[str, Any]
    output_files: list[str]

    @classmethod
    def build(
        cls,
        source_file: str,
        invoice: CanonicalInvoice | None,
        document_type: str,
        errors: list[str],
        route: RouteDecision | None,
        output_files: list[str],
    ) -> "ProcessingReport":
        return cls(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            source_file=source_file,
            invoice_number=invoice.invoice_number if invoice else "",
            document_type=document_type,
            status="FAILED" if errors else "SUCCESS",
            errors=errors,
            route=route.to_dict() if route else {},
            output_files=output_files,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
