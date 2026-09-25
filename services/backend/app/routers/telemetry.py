from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, alert_service
from app.anomaly import detect_anomaly

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
        connectivity=data.connectivity,
    )
    db.add(new_telemetry)

    if device.status == "offline":
        device.status = "active"

    db.commit()
    db.refresh(new_telemetry)

    anomaly_result = detect_anomaly(data.temperature, data.vibration)

    for alert_type, message in anomaly_result.anomalies.items():
        alert = alert_service.create_alert_if_not_duplicate(db, data.device_id, alert_type, message)
        if alert:
            print(f"[ALERT CREATED] {device.device_id}: {message}")

    for alert_type in anomaly_result.normal:
        resolved = alert_service.resolve_alerts_for_type(db, data.device_id, alert_type)
        if resolved:
            print(f"[ALERT RESOLVED] {device.device_id}: {alert_type}")

    return new_telemetry


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