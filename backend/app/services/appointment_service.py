from datetime import date, datetime, time, timedelta
from typing import Optional
from app.models.appointment import Appointment, AppointmentStatus, PaymentStatus, ServiceType, SERVICE_DURATIONS, SERVICE_PRICES

_BUSINESS_START = time(9, 0)
_BUSINESS_END = time(18, 0)
_SLOT_STEP = 15  # minutes


class AppointmentService:
    def __init__(self) -> None:
        self._store: dict[str, Appointment] = {}

    def get_available_slots(self, appt_date: date, duration_minutes: int = 30) -> list[str]:
        current = datetime.combine(appt_date, _BUSINESS_START)
        end = datetime.combine(appt_date, _BUSINESS_END)
        slots = []
        while current + timedelta(minutes=duration_minutes) <= end:
            if not self._is_taken(current, current + timedelta(minutes=duration_minutes)):
                slots.append(current.strftime("%H:%M"))
            current += timedelta(minutes=_SLOT_STEP)
        return slots

    def create_appointment(
        self,
        customer_name: str,
        scheduled_at: datetime,
        service_type: ServiceType = ServiceType.haircut,
        stylist_name: str = "",
        duration_minutes: Optional[int] = None,
        notes: str = "",
    ) -> Appointment:
        if duration_minutes is None:
            duration_minutes = SERVICE_DURATIONS[service_type]
        slot_end = scheduled_at + timedelta(minutes=duration_minutes)
        if self._is_taken(scheduled_at, slot_end):
            raise ValueError(f"The slot at {scheduled_at} is already booked.")
        appt = Appointment(
            customer_name=customer_name,
            service_type=service_type,
            stylist_name=stylist_name,
            request=notes,
            scheduled_at=scheduled_at,
            duration_minutes=duration_minutes,
            price=SERVICE_PRICES.get(service_type, 0.0),
            status=AppointmentStatus.confirmed,
        )
        self._store[appt.id] = appt
        return appt

    def get_appointments(
        self,
        customer_name: Optional[str] = None,
        date_filter: Optional[str] = None,
    ) -> list[Appointment]:
        results = list(self._store.values())
        if customer_name:
            results = [a for a in results if customer_name.lower() in a.customer_name.lower()]
        if date_filter:
            try:
                filter_date = datetime.fromisoformat(date_filter).date()
                results = [a for a in results if a.scheduled_at.date() == filter_date]
            except ValueError:
                pass
        return sorted(results, key=lambda a: a.scheduled_at)

    def get_appointment(self, appointment_id: str) -> Appointment:
        appt = self._store.get(appointment_id)
        if appt is None:
            raise ValueError(f"Appointment '{appointment_id}' not found.")
        return appt

    def mark_paid(self, appointment_id: str) -> Appointment:
        appt = self._store.get(appointment_id)
        if appt is None:
            raise ValueError(f"Appointment '{appointment_id}' not found.")
        if appt.status == AppointmentStatus.cancelled:
            raise ValueError(f"Cannot pay for a cancelled appointment.")
        appt.payment_status = PaymentStatus.paid
        return appt

    def cancel_appointment(self, appointment_id: str) -> Appointment:
        appt = self._store.get(appointment_id)
        if appt is None:
            raise ValueError(f"Appointment '{appointment_id}' not found.")
        if appt.status == AppointmentStatus.cancelled:
            raise ValueError(f"Appointment '{appointment_id}' is already cancelled.")
        appt.status = AppointmentStatus.cancelled
        return appt

    def _is_taken(self, start: datetime, end: datetime) -> bool:
        for appt in self._store.values():
            if appt.status == AppointmentStatus.cancelled:
                continue
            appt_end = appt.scheduled_at + timedelta(minutes=appt.duration_minutes)
            if start < appt_end and end > appt.scheduled_at:
                return True
        return False


appointment_service = AppointmentService()
