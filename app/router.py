from app.models import CanonicalInvoice, RouteDecision


def route_invoice(invoice: CanonicalInvoice) -> RouteDecision:
    """
    Partner/customer-specific routing simulation.
    In real SAP CPI / B2B middleware, this could be based on sender ID,
    receiver ID, document type, country, partner profile, or agreement.
    """
    customer = invoice.customer.lower()
    supplier = invoice.supplier.lower()

    if "customer srl" in customer or "romania" in customer:
        return RouteDecision(
            receiver="SAP_ERP_RO",
            protocol="SFTP",
            target_path="/sap/ro/inbound/invoice/",
            reason="Romanian customer routing rule",
        )

    if "gmbh" in customer or "gmbh" in supplier:
        return RouteDecision(
            receiver="SAP_ERP_DE",
            protocol="AS2",
            as2_partner_id="DE_CUSTOMER_AS2",
            reason="German partner routing rule",
        )

    if invoice.currency == "USD":
        return RouteDecision(
            receiver="SAP_ERP_US",
            protocol="HTTPS",
            target_path="/sap/us/invoice-api",
            reason="USD invoice routing rule",
        )

    return RouteDecision(
        receiver="MANUAL_REVIEW",
        protocol="NONE",
        reason="No routing rule matched",
    )
