from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import devices, telemetry

app = FastAPI(title="Industrial Asset Monitoring API")

Base.metadata.create_all(bind=engine)

app.include_router(devices.router)
app.include_router(telemetry.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}