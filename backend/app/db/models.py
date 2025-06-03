from sqlalchemy import Column, Integer, Float, DateTime
from db.database import Base

class HumidityReading(Base):
    __tablename__ = "humidity_readings"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)