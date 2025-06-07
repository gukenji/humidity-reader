from pydantic import BaseModel
from typing import Optional


class PlantBaseSchema(BaseModel):
    moisture_threshold: Optional[float]
    name: Optional[str]


class PlantCreateSchema(PlantBaseSchema):
    pass


class PlantSchema(PlantBaseSchema):
    id: int

    class Config:
        from_attributes = True