from pydantic import BaseModel
from typing import Optional


class PlantBaseSchema(BaseModel):
    moisture_threshold: Optional[float]
    name: Optional[str]
    check_interval: Optional[int] = 10  # 10 minutes if not specified


class PlantCreateSchema(PlantBaseSchema):
    pass


class PlantSchema(PlantBaseSchema):
    id: int

    class Config:
        from_attributes = True