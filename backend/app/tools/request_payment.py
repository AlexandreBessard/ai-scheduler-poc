import json
from langchain_core.tools import tool
from app.services.appointment_service import appointment_service


@tool
def request_payment(appointment_id: str) -> str:
    """Trigger an in-app payment form for a customer who wants to pay in advance.

    Call this when the customer confirms they want to pay upfront for their appointment.
    The frontend will display a secure payment form automatically.

    Args:
        appointment_id: The appointment ID returned at booking time.
    """
    try:
        appt = appointment_service.get_appointment(appointment_id)
    except ValueError as e:
        return f"Could not initiate payment: {e}"

    if appt.status.value == "cancelled":
        return "Cannot pay for a cancelled appointment."

    return json.dumps({
        "__payment_request__": True,
        "appointment_id": appt.id,
        "amount": appt.price,
    })