from pydantic import BaseModel
from datetime import datetime
from models.plant import PlantSchema
from typing import Optional


class HumidityBaseSchema(BaseModel):
    value: float


class HumidityCreateSchema(HumidityBaseSchema):
    plant_id: Optional[int]
    pass


class HumiditySchema(HumidityBaseSchema):
    id: int
    timestamp: datetime
    plant: Optional[PlantSchema] = None
    
    class Config:
        from_attributes = True