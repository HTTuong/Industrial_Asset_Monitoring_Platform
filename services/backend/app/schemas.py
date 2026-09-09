from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DeviceCreate(BaseModel):
    device_id: str = Field(min_length=3, max_length=50)
    name: str = Field(min_length=1, max_length=100)

class DeviceResponse(BaseModel):
    id: int
    device_id: str
    name: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True  # allow converting directly from SQLAlchemy model