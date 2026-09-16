from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/telemetry", tags=["telemetry"])

@router.post("", response_model=schemas.TelemetryResponse, status_code=201)
def ingest_telemetry(data: schemas.TelemetryCreate, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.device_id == data.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Device '{data.device_id}' not registered")

    new_telemetry = models.Telemetry(
        device_id=data.device_id,
        temperature=data.temperature,
        vibration=data.vibration,
        battery=data.battery,
    )
    db.add(new_telemetry)

    if device.status == "offline":
        device.status = "active"

    db.commit()
    db.refresh(new_telemetry)
    return new_telemetry