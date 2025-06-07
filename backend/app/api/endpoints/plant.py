from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.plant import PlantSchema, PlantCreateSchema
from db.models import Plant
from db.database import get_db
from typing import List

router = APIRouter(prefix="/plant", tags=["Plant informations"])


@router.post("/", response_model=PlantSchema)
def create(request: PlantCreateSchema, db: Session = Depends(get_db)):

    new_plant = Plant(
        name=request.name,
        moisture_threshold=request.moisture_threshold,
        check_interval=request.check_interval or 10  # Default to 10 minutes if not specified
    )
    db.add(new_plant)
    db.commit()
    db.refresh(new_plant)
    return new_plant


@router.get("/", response_model=List[PlantSchema])
def findAll(db: Session = Depends(get_db)):
    plants = db.query(Plant).all()
    return plants


@router.get("/{id}", response_model=PlantSchema)
def findById(id: int, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found!")
    db.delete(plant)
    db.commit()
    return {"message": f"Plant {plant.name} successfully deleted!"}


@router.put("/{id}", response_model=PlantSchema)
def update(id: int, request: PlantCreateSchema, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found!")
    if request.name is not None:
        plant.name = request.name
    if request.moisture_threshold is not None:
        plant.moisture_threshold = request.moisture_threshold
    if request.check_interval is not None:
        plant.check_interval = request.moisture_threshold
    db.commit()
    db.refresh(plant)
    return plant