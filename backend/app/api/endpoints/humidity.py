from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
import pytz
from datetime import date
from models.humidity import HumiditySchema, HumidityCreateSchema
from db.models import HumidityReading, Plant
from db.database import get_db
from fastapi import Query
from services.convert_time import convert_list_timezone

tz = pytz.timezone("America/Sao_Paulo")
router = APIRouter(prefix="/humidity", tags=["Humidity Readings"])


@router.get("/", response_model=List[HumiditySchema])
def findAll(db: Session = Depends(get_db)):
    readings = db.query(HumidityReading).all()
    return convert_list_timezone(readings, tz)


@router.get("/by-date/", response_model=List[HumiditySchema])
def findByDate(
    start_date: date = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: date = Query(None, description="Optional end date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    if end_date is None:
        end_date = start_date

    start_naive = datetime.combine(start_date, datetime.min.time())
    end_naive = datetime.combine(end_date, datetime.max.time())

    start_sp = tz.localize(start_naive)
    end_sp = tz.localize(end_naive)

    start_utc = start_sp.astimezone(pytz.utc)
    end_utc = end_sp.astimezone(pytz.utc)

    readings = (
        db.query(HumidityReading)
        .filter(HumidityReading.timestamp >= start_utc)
        .filter(HumidityReading.timestamp <= end_utc)
        .order_by(HumidityReading.timestamp.asc())
        .all()
    )

    for r in readings:
        r.timestamp = r.timestamp.astimezone(tz)

    return readings


@router.get("/{id}", response_model=HumiditySchema)
def findById(id: int, db: Session = Depends(get_db)):
    reading = db.query(HumidityReading).filter(HumidityReading.id == id).first()
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    return reading


@router.post("/", response_model=HumiditySchema)
def create(request: HumidityCreateSchema, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(request.plant_id == Plant.id).first()
    new_reading = HumidityReading(
        value=request.value,
        timestamp=datetime.now(tz),
        plant=plant if plant else None
    )
    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)
    return new_reading


@router.put("/{id}", response_model=HumiditySchema)
def update(id: int, reading: HumidityCreateSchema, db: Session = Depends(get_db)):
    reading = db.query(HumidityReading).filter(HumidityReading.id == id).first()
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    reading.value = reading.value
    reading.timestamp = datetime.now(tz)
    db.commit()
    db.refresh(reading)
    return reading


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    reading = db.query(HumidityReading).filter(HumidityReading.id == id).first()
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    db.delete(reading)
    db.commit()
    return {"message": f"Reading {id} successfully deleted"}



