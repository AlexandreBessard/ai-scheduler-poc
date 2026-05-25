# Pydantic v2 models shared across tools, services, and API responses.
#
# AppointmentStatus(str, Enum)
#   Values: "pending" | "confirmed" | "cancelled"
#
# Appointment(BaseModel)
#   Fields:
#     id: str                        — UUID generated at creation
#     customer_name: str
#     request: str                   — original natural-language request from the customer
#     scheduled_at: datetime
#     duration_minutes: int          — default 30
#     status: AppointmentStatus      — default "pending"
#     created_at: datetime           — set automatically
#
# ChatRequest(BaseModel)             — request body for POST /chat
#   Fields:
#     message: str                   — user's natural-language prompt
#     thread_id: str                 — session UUID from the Angular client
