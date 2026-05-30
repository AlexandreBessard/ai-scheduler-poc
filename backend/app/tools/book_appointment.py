from langchain_core.tools import tool
from app.services.appointment_service import appointment_service
from app.models.appointment import ServiceType, SERVICE_DURATIONS
from app.utils.date_parser import parse_datetime


@tool
def book_appointment(
    customer_name: str,
    datetime_str: str,
    service_type: str = "haircut",
    stylist_name: str = "",
    notes: str = "",
) -> str:
    """Book a haircut appointment for a customer at a specific date and time.

    Args:
        customer_name: Full name of the customer.
        datetime_str: Natural language or ISO-8601 datetime
            (e.g. "tomorrow at 2pm", "next Monday at 9am", "2026-05-27T14:00").
        service_type: Type of service requested. Must be one of:
            "haircut" (45 min), "trim" (30 min), "color" (120 min),
            "highlights" (90 min), "blowout" (45 min), "other" (45 min).
            Default is "haircut".
        stylist_name: Preferred stylist name (optional, leave empty if no preference).
        notes: Additional notes, e.g. hair length, specific style requested.
    """
    try:
        scheduled_at = parse_datetime(datetime_str)
    except ValueError as e:
        return f"Could not parse datetime '{datetime_str}': {e}"

    try:
        stype = ServiceType(service_type.lower())
    except ValueError:
        valid = ", ".join(s.value for s in ServiceType)
        return f"Unknown service type '{service_type}'. Valid options: {valid}."

    try:
        appt = appointment_service.create_appointment(
            customer_name=customer_name,
            scheduled_at=scheduled_at,
            service_type=stype,
            stylist_name=stylist_name,
            notes=notes,
        )
    except ValueError as e:
        return f"Could not book appointment: {e}"

    stylist_line = f"\nStylist: {appt.stylist_name}" if appt.stylist_name else ""
    return (
        f"Appointment booked!\n"
        f"ID: {appt.id}\n"
        f"Customer: {appt.customer_name}\n"
        f"Service: {appt.service_type.value.title()}{stylist_line}\n"
        f"When: {appt.scheduled_at.strftime('%A, %B %d, %Y at %I:%M %p %Z')}\n"
        f"Duration: {appt.duration_minutes} minutes\n"
        f"Status: {appt.status}"
    )