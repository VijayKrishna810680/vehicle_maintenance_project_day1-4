from sqlalchemy.orm import Session
from . import models, schemas

def get_vehicle(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()

def get_vehicle_by_vin(db: Session, vin: str):
    return db.query(models.Vehicle).filter(models.Vehicle.vin == vin).first()

def create_vehicle(db: Session, vehicle: schemas.VehicleCreate):
    db_obj = models.Vehicle(**vehicle.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def list_vehicles(db: Session, skip=0, limit=100):
    return db.query(models.Vehicle).offset(skip).limit(limit).all()

def create_record(db: Session, vehicle_id: int, record: schemas.MaintenanceRecordCreate):
    db_record = models.MaintenanceRecord(**record.model_dump(), vehicle_id=vehicle_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def list_records_for_vehicle(db: Session, vehicle_id: int):
    return db.query(models.MaintenanceRecord).filter(models.MaintenanceRecord.vehicle_id == vehicle_id).all()
