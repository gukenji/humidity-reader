from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship


class HumidityReading(Base):
    __tablename__ = "humidity_readings"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    plant_id = Column(Integer, ForeignKey('plant.id'), nullable=False)

    plant = relationship("Plant", back_populates="humidity_readings")


class Plant(Base):
    __tablename__ = "plant"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    moisture_threshold = Column(Integer, nullable=False)
    check_interval = Column(Integer, default=60)  # in minutes
    humidity_readings = relationship("HumidityReading", back_populates="plant")
