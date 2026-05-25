# @tool  list_appointments
#
# Lists existing appointments, optionally filtered by customer name or date.
#
# Args:
#   customer_name: str | None — filter by customer (optional)
#   date: str | None          — filter by ISO-8601 date (optional)
#
# Returns:
#   str — formatted list of matching appointments (id, customer, datetime, status),
#         or a message if no appointments match the filter.
#
# Delegates to: appointment_service.get_appointments()
#
# Note: also used directly (without the agent) by api/routes/appointments.py
# for the admin dashboard — call the service directly there, not this tool.
