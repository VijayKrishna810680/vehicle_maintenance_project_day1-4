<#
Simple deployment helper for Google Cloud Run.
Usage: Open PowerShell, authenticate with `gcloud auth login`, then run:
  ./scripts/deploy_to_gcp.ps1 -ProjectId my-gcp-project -Region us-central1

This script will:
- enable required APIs
- build/push backend and frontend images (to Container Registry)
- deploy both as Cloud Run services

Notes:
- It does NOT create a Cloud SQL instance automatically. If you need Postgres, create a Cloud SQL instance and update DATABASE_URL below or use Cloud SQL Auth Proxy flags.
- Customize image names, service names, and env vars as needed.
#>

param(
  [Parameter(Mandatory=$true)]
  [string]$ProjectId,

  [string]$Region = "us-central1",

  [string]$BackendService = "vehicle-backend",
  [string]$FrontendService = "vehicle-frontend",

  [string]$BackendImage = "vehicle-backend:latest",
  [string]$FrontendImage = "vehicle-frontend:latest",

  [string]$CloudSQLInstance = "", # optionally set project:region:instance to attach

  [switch]$UseArtifactRegistry
)

function Check-Command($name) {
    $p = Get-Command $name -ErrorAction SilentlyContinue
    if (-not $p) { Write-Error "Required command '$name' not found. Please install it and retry."; exit 1 }
}

Check-Command gcloud
Check-Command docker

Write-Host "Setting gcloud project to $ProjectId and region to $Region"
gcloud config set project $ProjectId | Out-Null
gcloud config set run/region $Region | Out-Null

Write-Host "Enabling required APIs (Cloud Run, Cloud Build, Container Registry/Artifact Registry, Cloud SQL Admin (optional))"
if ($UseArtifactRegistry) {
  gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com sqladmin.googleapis.com --project $ProjectId
} else {
  gcloud services enable run.googleapis.com cloudbuild.googleapis.com containerregistry.googleapis.com sqladmin.googleapis.com --project $ProjectId
}

Write-Host "Building and pushing backend and frontend images"
if ($UseArtifactRegistry) {
  $repo = "us-docker.pkg.dev/$ProjectId/cloud-run-repo"
  Write-Host "Using Artifact Registry: $repo"
  # create repo if not exists (idempotent)
  gcloud artifacts repositories create cloud-run-repo --repository-format=docker --location=$Region --project=$ProjectId -q 2>$null || Write-Host 'Artifact repo exists or creation failed (ok to continue)'

  gcloud builds submit --tag $repo/$BackendImage ./backend
  docker build -f frontend/Dockerfile.cloud -t $repo/$FrontendImage frontend
  gcloud auth configure-docker $Region-docker.pkg.dev --quiet
  docker push $repo/$FrontendImage
  $backendImageRef = "$repo/$BackendImage"
  $frontendImageRef = "$repo/$FrontendImage"
} else {
  gcloud builds submit --tag gcr.io/$ProjectId/$BackendImage ./backend
  gcloud auth configure-docker --quiet
  docker build -f frontend/Dockerfile.cloud -t gcr.io/$ProjectId/$FrontendImage frontend
  docker push gcr.io/$ProjectId/$FrontendImage
  $backendImageRef = "gcr.io/$ProjectId/$BackendImage"
  $frontendImageRef = "gcr.io/$ProjectId/$FrontendImage"
}

Write-Host "Deploying backend to Cloud Run: $BackendService"
if ([string]::IsNullOrEmpty($CloudSQLInstance)) {
  Write-Host "No Cloud SQL instance provided. Backend will be deployed with placeholder DATABASE_URL. Update service after creating DB."
  $dbPlaceholder = "postgresql://USER:PASS@HOST:PORT/DBNAME"
  gcloud run deploy $BackendService --image $backendImageRef --platform managed --region $Region --allow-unauthenticated --set-env-vars "DATABASE_URL=$dbPlaceholder"
} else {
  Write-Host "Attaching Cloud SQL instance: $CloudSQLInstance"
  # When attaching Cloud SQL to Cloud Run, you typically use --add-cloudsql-instances and set DATABASE_URL accordingly.
  $connectionName = $CloudSQLInstance
  # Note: You must have the Cloud Run service account with Cloud SQL Client role to access the instance.
  $dbEnv = "DATABASE_URL=postgresql://postgres:$(terraform output -raw db_root_password 2>$null)@127.0.0.1:5432/vehicle_maintenance"
  gcloud run deploy $BackendService --image $backendImageRef --platform managed --region $Region --allow-unauthenticated --add-cloudsql-instances $connectionName --set-env-vars "$dbEnv"
}

Write-Host "Deploying frontend to Cloud Run: $FrontendService"
# It's common for frontend to need the backend URL. Replace below after backend deploy completes or set CORS accordingly.
$backendUrlPlaceholder = "https://$BackendService-$Region.a.run.app"
gcloud run deploy $FrontendService --image $frontendImageRef --platform managed --region $Region --allow-unauthenticated --set-env-vars "REACT_APP_BACKEND_URL=$backendUrlPlaceholder"

Write-Host "Deployment finished. Use 'gcloud run services list' to see deployed services. Visit the URL shown by the deploy command to open the service(s)."

Write-Host "If you plan to use Cloud SQL (Postgres), create an instance and either set DATABASE_URL to its public IP or deploy Cloud SQL Auth Proxy and add --add-cloudsql-instances to the gcloud run deploy command."
