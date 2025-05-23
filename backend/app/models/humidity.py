from pydantic import BaseModel
from typing import Optional

class HumidityBase(BaseModel):
    value: float

class HumidityCreate(HumidityBase):
    pass

class Humidity(HumidityBase):
    id: int
    timestamp: str

    class Config:
        from_attributes = True