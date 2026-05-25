# @tool  check_availability
#
# Checks available time slots for a given date and duration.
#
# Args:
#   date: str             — natural language or ISO-8601 date
#                           (e.g. "tomorrow", "next Friday", "2026-05-27")
#                           Parsed into a date object via utils.date_parser.parse_date()
#   duration_minutes: int — desired appointment length (default: 30)
#
# Returns:
#   str — human-readable list of available slots, or a message if none found.
#         Claude uses this string to formulate its response to the user.
#
# Delegates to: appointment_service.get_available_slots()
# Date parsing: utils.date_parser.parse_date(date)
