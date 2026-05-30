from langchain_core.tools import tool
from app.services.appointment_service import appointment_service


@tool
def pay_appointment(appointment_id: str) -> str:
    """Mark an appointment as paid in advance.

    Call this tool when the customer confirms they want to pay for their appointment upfront.
    The price is already set on the appointment at booking time.

    Args:
        appointment_id: The ID returned when the appointment was booked.
    """
    try:
        appt = appointment_service.mark_paid(appointment_id)
        return (
            f"Payment confirmed! Appointment {appt.id} for {appt.customer_name} "
            f"({appt.service_type.value.title()}, €{appt.price:.2f}) is now marked as paid."
        )
    except ValueError as e:
        return f"Could not process payment: {e}"
