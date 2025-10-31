# Vehicle Maintenance Records API
Combined Day 1 (FastAPI + Postgres) and Day 2 (React + AI agent) scaffold.

## Quick start (recommended)
1. Install Docker & Docker Compose.
2. From project root run:
   ```bash
   docker-compose up --build
   ```
3. Backend Swagger: http://localhost:8000/docs
4. Frontend: http://localhost:3000
5. Chat endpoint: POST http://localhost:8000/chat { "message": "Hello" }

## Notes
- The AI agent tries to use `langchain`/`openai` if available; otherwise it falls back to a lightweight built-in stub.
- See `backend/README.md` and `frontend/README.md` for more details.

# Vehicle Maintenance — Full project (Day 1-3)

This repository contains a full-stack Vehicle Maintenance Records app (Day 1 → Day 3) set up to run via Docker Compose and ready to deploy to a Google Cloud VM.

## What is included
- Backend: FastAPI (Python) with SQLAlchemy + Postgres integration, `/chat` route calling an agent module.
- Frontend: React app that is built during Docker build and served by the backend container.
- Docker Compose: `docker-compose.yml` boots Postgres + backend (which includes the built frontend).
- GCP-ready: cloud-init script included to bootstrap a VM and run Docker Compose.
- Agent: `app/agent.py` checks `GEMINI_API_KEY` env var and will call a user-provided Gemini endpoint if set (placeholder).

## Quick local run (Linux / macOS / Windows WSL)
1. Install Docker and Docker Compose plugin.
2. Build and run:
   ```bash
   docker compose build --no-cache
   docker compose up -d
   ```
3. Open `http://localhost/` to view the app. FastAPI docs available at `http://localhost/docs`.

## Deploy on Google Cloud (VM) - summary
1. Create an Ubuntu VM (2vCPU, 4GB) and open port 80 in firewall.
2. Upload this project zip and extract.
3. SSH to VM and run:
   ```bash
   sudo apt update
   sudo apt install -y curl unzip
   curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh
   sudo apt-get install -y docker-compose-plugin
   sudo usermod -aG docker $USER
   # logout/login or restart shell so docker group is active
   docker compose up -d --build
   ```
4. Optionally set `GEMINI_API_KEY` env in the `docker-compose.yml` before running (or export in VM environment) to enable real Gemini calls.

## Notes
- **Gemini integration**: Agent code includes a placeholder HTTP call. Replace `GEMINI_API_URL` with your provider's endpoint and set `GEMINI_API_KEY` in environment.
- **Database persistence**: Postgres data is stored in Docker volume `pgdata`.
- **HTTPS**: For production, put an nginx reverse-proxy and certbot or use Google Load Balancer with managed certs.

## Deploy to Google Cloud (Cloud Run) — recommended for managed containers

This project contains container-ready services for Cloud Run. The repository now includes a production frontend image definition (`frontend/Dockerfile.cloud`) and a convenience deploy script (`scripts/deploy_to_gcp.ps1`).

High-level steps
1. Install the Google Cloud SDK (gcloud) and authenticate:
   ```pwsh
   gcloud auth login
   gcloud auth configure-docker
   ```
2. Create or select a GCP project and enable billing.
3. From project root, run the PowerShell deploy helper (replace PROJECT_ID/REGION):
   ```pwsh
   ./scripts/deploy_to_gcp.ps1 -ProjectId YOUR_PROJECT_ID -Region us-central1
   ```

What the script does
- Enables required APIs (Cloud Run, Cloud Build, Container Registry, Cloud SQL admin)
- Builds backend using `gcloud builds submit` and pushes to Container Registry
- Builds frontend production image (uses `frontend/Dockerfile.cloud`) and pushes to Container Registry
- Deploys both images to Cloud Run as separate services. You will need to set up a managed Postgres (Cloud SQL) and provide a DATABASE_URL if you need persistent DB.

Notes and next steps
- If you need Postgres, create a Cloud SQL (Postgres) instance and either expose it with a public IP (not recommended) or use Cloud SQL Auth Proxy with Cloud Run (recommended) and add `--add-cloudsql-instances` to the `gcloud run deploy` command in the script.
- For CI/CD, consider adding a `cloudbuild.yaml` and connecting the repo to Cloud Build triggers.
- The Cloud Run frontend expects the backend URL to be available via the `REACT_APP_BACKEND_URL` env var — the deploy script sets a placeholder you should replace with the actual backend service URL after deploy.

If you'd like, I can:
- Create an automated `cloudbuild.yaml` to run this deploy on push to `main`.
- Add Terraform to provision Project, Artifact Registry / Cloud SQL instance, IAM, and Cloud Run services.


If you want, I can also:
- Provide Terraform scripts to create VPC + VM + firewall in GCP.
- Add an nginx container for HTTPS and HTTP->HTTPS redirect.
- Replace the placeholder Gemini HTTP call with exact code for the Gemini HTTP API if you provide the API docs or confirm the endpoint.

