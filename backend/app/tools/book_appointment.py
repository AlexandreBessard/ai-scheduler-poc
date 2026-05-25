# @tool  book_appointment
#
# Books an appointment for a customer at a specific date and time.
#
# Args:
#   customer_name: str    — full name of the customer
#   datetime_str: str     — natural language or ISO-8601 datetime
#                           (e.g. "tomorrow afternoon", "next Monday at 9am", "2026-05-27T14:00")
#                           Parsed into a timezone-aware datetime via utils.date_parser.parse_datetime()
#   duration_minutes: int — appointment length (default: 30)
#   notes: str            — optional context from the customer's request
#
# Returns:
#   str — confirmation message with the generated appointment ID,
#         or an error message if the slot is no longer available.
#
# Delegates to: appointment_service.create_appointment()
# Date parsing: utils.date_parser.parse_datetime(datetime_str)
