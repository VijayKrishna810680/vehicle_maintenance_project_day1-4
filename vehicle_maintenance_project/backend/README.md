# Backend (FastAPI)
Navigate to /backend.

## Running locally without Docker:
1. python -m venv venv
2. source venv/bin/activate   (Windows: venv\Scripts\activate)
3. pip install -r requirements.txt
4. export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/vehicle_maintenance
5. uvicorn app.main:app --reload

## Migrations:
Alembic is configured; edit alembic.ini for the DB URL and run:
alembic revision --autogenerate -m "init"
alembic upgrade head
