from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/devices", tags=["devices"])

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