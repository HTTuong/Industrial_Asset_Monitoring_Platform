from sqlalchemy.orm import Session
from app import models


def create_alert_if_not_duplicate(db: Session, device_id: str, alert_type: str, message: str):
    existing = (
        db.query(models.Alert)
        .filter(
            models.Alert.device_id == device_id,
            models.Alert.alert_type == alert_type,
            models.Alert.resolved == False,
        )
        .first()
    )
    if existing:
        return None 

    alert = models.Alert(device_id=device_id, alert_type=alert_type, message=message, resolved=False)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def resolve_alerts_for_type(db: Session, device_id: str, alert_type: str):
    active_alerts = (
        db.query(models.Alert)
        .filter(
            models.Alert.device_id == device_id,
            models.Alert.alert_type == alert_type,
            models.Alert.resolved == False,
        )
        .all()
    )
    for alert in active_alerts:
        alert.resolved = True
    if active_alerts:
        db.commit()
    return active_alerts