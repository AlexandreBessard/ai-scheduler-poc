# @tool  cancel_appointment
#
# Cancels an existing appointment by its ID.
#
# Args:
#   appointment_id: str — the ID returned when the appointment was booked
#
# Returns:
#   str — confirmation that the appointment was cancelled,
#         or an error message if the ID does not exist or is already cancelled.
#
# Delegates to: appointment_service.cancel_appointment()
