from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HumidityBase(BaseModel):
    value: float

class HumidityCreate(HumidityBase):
    pass

class Humidity(HumidityBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True