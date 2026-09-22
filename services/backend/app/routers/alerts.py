from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("", response_model=list[schemas.AlertResponse])
def list_alerts(resolved: bool | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Alert)
    if resolved is not None:
        query = query.filter(models.Alert.resolved == resolved)
    return query.order_by(models.Alert.created_at.desc()).all()