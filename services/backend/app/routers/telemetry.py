from app.anomaly import detect_anomaly

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
    if anomaly_result.is_anomaly:
        print(f"[ANOMALY] Device {data.device_id}: {anomaly_result.reasons}")

    return new_telemetry