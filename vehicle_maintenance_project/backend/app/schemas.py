from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class MaintenanceRecordBase(BaseModel):
    date: date
    type: str
    mileage: int
    notes: Optional[str] = None
    next_service_date: Optional[date] = None

class MaintenanceRecordCreate(MaintenanceRecordBase):
    pass

class MaintenanceRecord(MaintenanceRecordBase):
    id: int
    vehicle_id: int
    class Config:
        orm_mode = True

class VehicleBase(BaseModel):
    vin: str
    make: Optional[str]
    model: Optional[str]
    year: Optional[int]

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    records: List[MaintenanceRecord] = []
    class Config:
        orm_mode = True
