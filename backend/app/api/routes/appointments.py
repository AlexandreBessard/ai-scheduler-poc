# REST endpoints consumed by the Angular admin-app.
# These routes bypass the agent entirely — direct service calls only.

from fastapi import APIRouter, HTTPException
from app.models.appointment import Appointment
from app.services.appointment_service import appointment_service

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("", response_model=list[Appointment])
async def list_appointments() -> list[Appointment]:
    return appointment_service.get_appointments()


@router.get("/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: str) -> Appointment:
    try:
        return appointment_service.get_appointment(appointment_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Appointment not found")


@router.post("/{appointment_id}/pay", response_model=Appointment)
async def pay_appointment(appointment_id: str) -> Appointment:
    try:
        return appointment_service.mark_paid(appointment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))