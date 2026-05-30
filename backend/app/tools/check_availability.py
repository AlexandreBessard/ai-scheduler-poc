from langchain_core.tools import tool
from app.services.appointment_service import appointment_service
from app.utils.date_parser import parse_date


@tool
def check_availability(date: str, duration_minutes: int = 45) -> str:
    """Check available time slots at the salon for a given date and service duration.

    Args:
        date: Natural language or ISO-8601 date (e.g. "tomorrow", "next Friday", "2026-05-27").
        duration_minutes: Service length in minutes. Typical durations:
            haircut=45, trim=30, color=120, highlights=90, blowout=45. Default is 45.

    Service prices (EUR): haircut=€35, trim=€20, color=€80, highlights=€90, blowout=€25.
    Always mention the price when confirming which service the customer wants.
    """
    try:
        # convert for example: tomorrow at 5pm
        parsed = parse_date(date)
    except ValueError as e:
        return f"Could not parse date '{date}': {e}"

    slots = appointment_service.get_available_slots(parsed, duration_minutes)
    label = parsed.strftime("%A, %B %d, %Y")
    if not slots:
        return f"No available slots on {label} for a {duration_minutes}-minute appointment."
    return f"Available slots on {label}:\n" + "\n".join(f"  - {s}" for s in slots)
