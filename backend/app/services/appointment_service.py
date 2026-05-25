# Appointment data service — the single source of truth for all appointment logic.
# Tools and API routes call this service; they never touch storage directly.
#
# In-memory store (POC):
#   A dict keyed by appointment ID is used during development.
#   Replace the storage backend here (e.g. SQLAlchemy + PostgreSQL) without
#   touching any tool or route code.
#
# Functions to implement:
#
#   get_available_slots(date: str, duration_minutes: int) -> list[str]
#       Return a list of available HH:MM strings for the given date.
#
#   create_appointment(customer_name, date, time, duration_minutes, notes) -> Appointment
#       Validate the slot is free, persist, and return the created Appointment model.
#
#   get_appointments(customer_name=None, date=None) -> list[Appointment]
#       Return all appointments, optionally filtered.
#
#   cancel_appointment(appointment_id: str) -> Appointment
#       Mark the appointment as cancelled and return the updated model.
#       Raise a ValueError if the ID does not exist.
