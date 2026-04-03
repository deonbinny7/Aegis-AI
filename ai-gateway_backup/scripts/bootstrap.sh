#!/usr/bin/env bash
set -e

echo "Bootstrapping AI Gateway environment..."

# 1. Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

# 2. Check for docker-compose
if command -v docker-compose &> /dev/null; then
    echo "Starting Docker Compose services..."
    docker-compose up -d db redis
elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
    echo "Starting Docker Compose services..."
    docker compose up -d db redis
else
    echo "Docker not found or docker compose not available. Skipping container startup."
fi

echo "Waiting for database to be ready..."
./scripts/wait_for_db.sh

echo "Applying migrations..."
cd backend
alembic upgrade head
cd ..

echo "Seeding initial development data..."
# Run the python script directly (assumes virtualenv is active or deps installed)
python scripts/seed_dev_data.py

echo "Bootstrap complete!"
