from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
import pytz
from datetime import date

from models.humidity import Humidity, HumidityCreate
from db.models import HumidityReading
from db.database import get_db
from fastapi import Query

tz = pytz.timezone("America/Sao_Paulo")
router = APIRouter(prefix="/humidity", tags=["Humidity Readings"])

@router.get("/", response_model=List[Humidity])
def read_all(db: Session = Depends(get_db)):
    return db.query(HumidityReading).all()

@router.get("/by-date/", response_model=List[Humidity])
def read_by_date(
    start_date: date = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: date = Query(None, description="Optional end date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    # Se end_date não for fornecida, use start_date como único dia
    if end_date is None:
        end_date = start_date

    # Convert date -> datetime with timezone
    start_datetime = datetime.combine(start_date, datetime.min.time()).astimezone(tz)
    end_datetime = datetime.combine(end_date, datetime.max.time()).astimezone(tz)

    readings = (
        db.query(HumidityReading)
        .filter(HumidityReading.timestamp >= start_datetime)
        .filter(HumidityReading.timestamp <= end_datetime)
        .order_by(HumidityReading.timestamp.asc())
        .all()
    )

    return readings

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
        timestamp=datetime.now(tz)
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
    db_reading.timestamp = datetime.now(tz)
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



