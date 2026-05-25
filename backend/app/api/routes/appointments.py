# REST endpoints consumed by the Angular admin-app.
# These routes bypass the agent entirely — direct service calls only.
#
# Endpoints:
#   GET  /appointments          — return all appointments (used by admin dashboard)
#   GET  /appointments/{id}     — return a single appointment by ID
#
# Each handler:
#   1. Calls appointment_service to fetch data
#   2. Returns a list/instance of the Appointment Pydantic model
#
# No LangGraph involved here. The agent routes are in chat.py.
