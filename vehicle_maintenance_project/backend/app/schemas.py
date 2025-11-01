from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    vehicle_id: int

class VehicleBase(BaseModel):
    vin: str
    make: Optional[str]
    model: Optional[str]
    year: Optional[int]

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    records: List[MaintenanceRecord] = []
