@echo off
echo ========================================================
echo        Enterprise AI Platform - Startup Script
echo ========================================================
echo.

REM 1. Start the FastAPI Backend
echo [1/3] Starting Backend Server (FastAPI on Port 8000)...
start "AI Gateway - Backend" cmd /k "cd backend && venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000"

REM 2. Start the Celery Worker
echo [2/3] Starting Celery Worker for Background Tasks...
start "AI Gateway - Celery Worker" cmd /k "cd backend && venv\Scripts\celery.exe -A app.workers.celery_app worker --loglevel=info --pool=solo"

REM 3. Start the Vite Frontend
echo [3/3] Starting Frontend Server (Vite React App)...
start "AI Gateway - Frontend" cmd /k "cd frontend && npm run dev"

REM 4. Wait for Vite to start, then open the browser
echo Waiting for servers to initialize...
ping 127.0.0.1 -n 4 > nul
start "" "http://localhost:3000"

echo.
echo ========================================================
echo All services have been launched in separate windows!
echo - Backend API:  http://127.0.0.1:8000
echo - Frontend:     http://localhost:3000
echo.
echo Please ensure Redis and PostgreSQL are running in the 
echo background (via Docker or local services).
echo ========================================================
pause