from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4


class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class PaymentStatus(str, Enum):
    unpaid = "unpaid"
    paid = "paid"


class ServiceType(str, Enum):
    haircut = "haircut"
    trim = "trim"
    color = "color"
    highlights = "highlights"
    blowout = "blowout"
    other = "other"


# Default durations in minutes per service
SERVICE_DURATIONS: dict[ServiceType, int] = {
    ServiceType.haircut: 45,
    ServiceType.trim: 30,
    ServiceType.color: 120,
    ServiceType.highlights: 90,
    ServiceType.blowout: 45,
    ServiceType.other: 45,
}

# Prices in EUR per service
SERVICE_PRICES: dict[ServiceType, float] = {
    ServiceType.haircut: 35.0,
    ServiceType.trim: 20.0,
    ServiceType.color: 80.0,
    ServiceType.highlights: 90.0,
    ServiceType.blowout: 25.0,
    ServiceType.other: 40.0,
}


class Appointment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    customer_name: str
    service_type: ServiceType = ServiceType.haircut
    stylist_name: str = ""
    request: str = ""
    scheduled_at: datetime
    duration_minutes: int = 45
    price: float = 0.0
    status: AppointmentStatus = AppointmentStatus.pending
    payment_status: PaymentStatus = PaymentStatus.unpaid
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    message: str = Field(..., max_length=2000)
    thread_id: str


class PaymentRequest(BaseModel):
    appointment_id: str
    amount: float


class ChatResponse(BaseModel):
    message: str
    thread_id: str
    payment_request: PaymentRequest | None = None
