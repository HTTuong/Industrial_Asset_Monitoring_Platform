from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/devices", tags=["devices"])

@router.get("", response_model=list[schemas.DeviceResponse])
def list_devices(db: Session = Depends(get_db)):
    return db.query(models.Device).all()

@router.get("/{device_id}", response_model=schemas.DeviceResponse)
def get_device(device_id: str, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Device '{device_id}' not found")
    return device

@router.post("", response_model=schemas.DeviceResponse, status_code=201)
def register_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Device).filter(models.Device.device_id == device.device_id).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Device '{device.device_id}' already registered")

    new_device = models.Device(device_id=device.device_id, name=device.name, status="offline")
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device

@router.patch("/{device_id}/deactivate", response_model=schemas.DeviceResponse)
def deactivate_device(device_id: str, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Device '{device_id}' not found")

    device.status = "inactive"
    db.commit()
    db.refresh(device)
    return device

@router.get("/{device_id}", response_model=list[schemas.TelemetryResponse])
def get_device_telemetry(device_id: str, limit: int = 50, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Device '{device_id}' not found")

    return (
        db.query(models.Telemetry)
        .filter(models.Telemetry.device_id == device_id)
        .order_by(models.Telemetry.timestamp.desc())
        .limit(limit)
        .all()
    )

