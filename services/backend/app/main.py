from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app import models
from app.routers import devices, telemetry, alerts

app = FastAPI(title="Industrial Asset Monitoring API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(devices.router)
app.include_router(telemetry.router)
app.include_router(alerts.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}