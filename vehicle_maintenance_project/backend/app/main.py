import os
from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from .agent import agent_run

# ------------------ Database Setup ------------------ #
Base.metadata.create_all(bind=engine)

# ------------------ FastAPI App ------------------ #
app = FastAPI(title="Vehicle Maintenance Records API")

# ------------------ CORS Setup (VERY IMPORTANT) ------------------ #
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://vehicle-frontend.onrender.com",   # ✅ your actual frontend
        "*"                                        # optional
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ DB Dependency ------------------ #
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ API Routes ------------------ #
@app.post("/vehicles/", response_model=schemas.Vehicle)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    db_v = crud.get_vehicle_by_vin(db, vin=vehicle.vin)
    if db_v:
        raise HTTPException(status_code=400, detail="VIN already exists")
    return crud.create_vehicle(db, vehicle)

@app.get("/vehicles/", response_model=list[schemas.Vehicle])
def read_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_vehicles(db, skip, limit)

@app.get("/vehicles/{vehicle_id}", response_model=schemas.Vehicle)
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    v = crud.get_vehicle(db, vehicle_id)
    if not v:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return v

@app.post("/vehicles/{vehicle_id}/records", response_model=schemas.MaintenanceRecord)
def add_record(vehicle_id: int, record: schemas.MaintenanceRecordCreate, db: Session = Depends(get_db)):
    if not crud.get_vehicle(db, vehicle_id):
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return crud.create_record(db, vehicle_id, record)

@app.get("/vehicles/{vehicle_id}/records", response_model=list[schemas.MaintenanceRecord])
def get_records(vehicle_id: int, db: Session = Depends(get_db)):
    return crud.list_records_for_vehicle(db, vehicle_id)

@app.post("/chat")
def chat(payload: dict = Body(...)):
    message = payload.get("message", "")
    resp = agent_run(message)
    return {"response": resp}


# ✅ ***REMOVE FRONTEND SERVING — BECAUSE FRONTEND IS A SEPARATE STATIC SITE***
@app.get("/")
def home():
    return {
        "status": "Backend running",
        "message": "Frontend is deployed separately on Render Static Site."
    }
