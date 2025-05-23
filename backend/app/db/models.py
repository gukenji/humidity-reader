from sqlalchemy import Column, Integer, Float, String
from db.database import Base

class HumidityReading(Base):
    __tablename__ = "humidity_readings"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    timestamp = Column(String, nullable=False)