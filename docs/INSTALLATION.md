# Installation Guide — Altair AI

This guide covers setting up Altair AI on your local environment (bare-metal) and inside containers.

---

## 🐋 Option 1: Docker Compose Setup (Recommended)

Docker Compose starts all necessary services (PostgreSQL, Redis, Celery, Prometheus, Grafana, FastAPI, React Frontend) in isolated networks.

### Steps:
1. Ensure Docker Desktop is installed and running.
2. Clone the repository and configure `.env`:
   ```bash
   cp .env.example .env
   # Add your API Keys (GEMINI_API_KEY, GROQ_API_KEY, etc.)
   ```
3. Run the development docker stack:
   ```bash
   docker compose up --build
   ```
4. Wait for database migrations to execute. The backend will be available at `http://localhost:8000` and the dashboard at `http://localhost:5173`.

---

## 🐍 Option 2: Bare-Metal Setup (Local Development)

### Backend Requirements:
- Python 3.11 or 3.12
- PostgreSQL 15+
- Redis 6.2+

### Setup steps:
1. Navigate to the backend directory and set up a Python virtual environment:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
2. Install python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` in the project root and configure your PostgreSQL and Redis connections:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ai_gateway
   REDIS_URL=redis://localhost:6379/0
   ```
4. Run Alembic migrations:
   ```bash
   alembic upgrade head
   ```
5. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Requirements:
- Node.js 18+
- npm or yarn

### Setup steps:
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install npm modules:
   ```bash
   npm install
   ```
3. Start the Vite development build server:
   ```bash
   npm run dev
   ```
   *The client dashboard will load on `http://localhost:5173`.*

// Code style format review — 2026-06-15T20:24:07
