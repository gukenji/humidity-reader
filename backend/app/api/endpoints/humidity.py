from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime

from models.humidity import Humidity, HumidityCreate
from db.models import HumidityReading
from db.database import get_db

router = APIRouter(prefix="/humidity", tags=["Humidity Readings"])

@router.get("/", response_model=List[Humidity])
def read_all(db: Session = Depends(get_db)):
    return db.query(HumidityReading).all()

@router.get("/{reading_id}", response_model=Humidity)
def read_one(reading_id: int, db: Session = Depends(get_db)):
    reading = db.query(HumidityReading).filter(HumidityReading.id == reading_id).first()
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    return reading

@router.post("/", response_model=Humidity)
def create(reading: HumidityCreate, db: Session = Depends(get_db)):
    new_reading = HumidityReading(
        value=reading.value,
        timestamp=datetime.now().isoformat()
    )
    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)
    return new_reading

@router.put("/{reading_id}", response_model=Humidity)
def update(reading_id: int, reading: HumidityCreate, db: Session = Depends(get_db)):
    db_reading = db.query(HumidityReading).filter(HumidityReading.id == reading_id).first()
    if not db_reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    db_reading.value = reading.value
    db_reading.timestamp = datetime.now().isoformat()
    db.commit()
    db.refresh(db_reading)
    return db_reading

@router.delete("/{reading_id}")
def delete(reading_id: int, db: Session = Depends(get_db)):
    reading = db.query(HumidityReading).filter(HumidityReading.id == reading_id).first()
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    db.delete(reading)
    db.commit()
    return {"message": f"Reading {reading_id} successfully deleted"}