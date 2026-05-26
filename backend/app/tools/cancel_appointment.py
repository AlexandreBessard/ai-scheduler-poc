from langchain_core.tools import tool
from app.services.appointment_service import appointment_service


@tool
def cancel_appointment(appointment_id: str) -> str:
    """Cancel an existing appointment by its ID.

    Args:
        appointment_id: The ID returned when the appointment was booked.
    """
    try:
        appt = appointment_service.cancel_appointment(appointment_id)
        return f"Appointment {appt.id} for {appt.customer_name} has been cancelled."
    except ValueError as e:
        return f"Could not cancel appointment: {e}"
