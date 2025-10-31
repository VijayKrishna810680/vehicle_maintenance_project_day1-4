# Use official Python image
FROM python:3.11-slim

# Install PostgreSQL client utilities for pg_isready
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /usr/src/app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Wait for DB to be ready before starting backend
CMD ["bash", "-c", "until pg_isready -h db -p 5432; do echo 'waiting for db'; sleep 2; done; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
