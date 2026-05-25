from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4


class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class Appointment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    customer_name: str
    request: str
    scheduled_at: datetime
    duration_minutes: int = 30
    status: AppointmentStatus = AppointmentStatus.pending
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    message: str
    thread_id: str


class ChatResponse(BaseModel):
    message: str
    thread_id: str
