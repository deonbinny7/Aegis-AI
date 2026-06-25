# Deployment Guide — Altair AI

Guides for deploying Altair AI in production environments.

---

## 🚂 Option 1: Railway (Recommended for Quick Cloud Hosting)

Railway can host the complete monorepo using its multi-service canvas:

1. Connect your GitHub account to Railway.
2. Select **New Project** and link to `deonbinny7/AltairAI`.
3. Railway will read the repository structure:
   * **Backend**: Spin up a Python service, bind the start command to `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, and add environment variables.
   * **Frontend**: Spin up a Static/Node service pointing to `/frontend` with build command `npm run build` and start command `npm run preview`.
4. Spin up **PostgreSQL** and **Redis** database templates from the Railway database library.
5. Link variables (`DATABASE_URL` and `REDIS_URL`) across services using Railway reference syntax (e.g. `${{postgres.DATABASE_URL}}`).

---

## ☁️ Option 2: Production Ubuntu Server (AWS EC2 / DigitalOcean)

For deploying on a virtual machine (VM) using Docker:

### 1. VM Provisioning
1. Launch an Ubuntu 22.04 VM with at least 2 vCPUs and 4GB RAM.
2. Install Docker and git:
   ```bash
   sudo apt-get update
   sudo apt-get install -y docker.io docker-compose git
   ```

### 2. Configure project
1. Clone the repository:
   ```bash
   git clone https://github.com/deonbinny7/AltairAI.git /opt/altair-ai
   cd /opt/altair-ai
   ```
2. Copy and configure variables:
   ```bash
   cp .env.example .env
   # Edit .env with production passwords and API keys
   ```

### 3. Run production Compose
1. Startup services:
   ```bash
   docker compose -f docker-compose.prod.yml up -d
   ```
2. Setup Nginx as a reverse proxy, mapping port 80/443 to the frontend static server on port 80 and the backend API on port 8000.
3. Configure Let's Encrypt SSL certificates.
