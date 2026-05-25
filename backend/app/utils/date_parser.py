# Natural language date/time parser.
# Wraps python-dateparser to convert human expressions into datetime objects.
#
# Why this exists:
#   Claude may pass relative expressions (e.g. "tomorrow afternoon",
#   "next Tuesday at 3pm", "in two weeks") as tool arguments.
#   This utility normalises them into timezone-aware datetime objects
#   before they reach the service layer.
#
# Functions to implement:
#
#   parse_datetime(value: str, timezone: str = "UTC") -> datetime
#       Parse a natural language string into a datetime.
#       - Uses dateparser.parse() with PREFER_DATES_FROM="future" so that
#         "Tuesday" means the next upcoming Tuesday, not the past one.
#       - Raises ValueError if the string cannot be parsed.
#       Example:
#           parse_datetime("tomorrow afternoon")   → 2026-05-26 14:00:00+00:00
#           parse_datetime("next Monday at 9am")   → 2026-06-01 09:00:00+00:00
#
#   parse_date(value: str, timezone: str = "UTC") -> date
#       Convenience wrapper — calls parse_datetime() and returns only the date part.
#       Used by check_availability and book_appointment when only a date is needed.
#
# Usage in tools:
#   from app.utils.date_parser import parse_datetime, parse_date
#
#   scheduled_dt = parse_datetime(date_str)   # inside book_appointment
#   date_only    = parse_date(date_str)       # inside check_availability
#
# dateparser settings applied globally:
#   PREFER_DATES_FROM : "future"
#   RETURN_AS_TIMEZONE_AWARE : True
#   TO_TIMEZONE : caller-supplied timezone (default "UTC")
