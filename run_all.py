import subprocess
import webbrowser
import time
import os

# Paths
backend_path = r"vehicle_maintenance_project\backend"
frontend_path = r"vehicle_maintenance_project\frontend"

# Step 1: Run FastAPI backend
print("🚀 Starting FastAPI backend...")
backend_process = subprocess.Popen(
    ["uvicorn", "app.main:app", "--reload", "--port", "8000"],
    cwd=backend_path,
)

# Wait a few seconds for backend to start
time.sleep(5)

# Step 2: Run React frontend (npm start)
print("🌐 Starting React frontend...")
frontend_process = subprocess.Popen(
    ["npm", "start"],
    cwd=frontend_path,
    shell=True
)

# Step 3: Open browser to unified link (backend serving React)
time.sleep(5)
print("🔗 Opening app in browser...")
webbrowser.open("http://127.0.0.1:8000")

# Step 4: Keep both running until user stops
try:
    backend_process.wait()
    frontend_process.wait()
except KeyboardInterrupt:
    print("\n🛑 Stopping both servers...")
    backend_process.terminate()
    frontend_process.terminate()
