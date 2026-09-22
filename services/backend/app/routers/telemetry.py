from app.anomaly import detect_anomaly
from app import alert_service

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