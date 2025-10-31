from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String, unique=True, index=True, nullable=False)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    records = relationship("MaintenanceRecord", back_populates="vehicle", cascade="all, delete-orphan")

class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    date = Column(Date)
    type = Column(String)
    mileage = Column(Integer)
    notes = Column(Text)
    next_service_date = Column(Date, nullable=True)

    vehicle = relationship("Vehicle", back_populates="records")
