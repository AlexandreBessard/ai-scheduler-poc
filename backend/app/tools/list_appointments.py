from langchain_core.tools import tool
from app.services.appointment_service import appointment_service


@tool
def list_appointments(customer_name: str | None = None, date: str | None = None) -> str:
    """List existing appointments, optionally filtered by customer name or date.

    Args:
        customer_name: Filter by customer name (optional).
        date: Filter by date in ISO-8601 format, e.g. "2026-05-27" (optional).
    """
    results = appointment_service.get_appointments(customer_name=customer_name, date_filter=date)
    if not results:
        return "No appointments found."
    lines = []
    for a in results:
        stylist = f" with {a.stylist_name}" if a.stylist_name else ""
        lines.append(
            f"- ID: {a.id} | {a.customer_name} | "
            f"{a.service_type.value.title()}{stylist} | "
            f"{a.scheduled_at.strftime('%Y-%m-%d %H:%M')} | "
            f"{a.duration_minutes}min | {a.status}"
        )
    return "\n".join(lines)
