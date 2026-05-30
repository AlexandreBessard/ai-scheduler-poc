from datetime import datetime, date
import dateparser

_SETTINGS = {
    "PREFER_DATES_FROM": "future",
    "RETURN_AS_TIMEZONE_AWARE": False,
}


def parse_datetime(value: str) -> datetime:
    result = dateparser.parse(value, settings=_SETTINGS)
    if result is None:
        raise ValueError(f"Could not parse datetime: '{value}'")
    return result

def parse_date(value: str) -> date:
    return parse_datetime(value).date()
