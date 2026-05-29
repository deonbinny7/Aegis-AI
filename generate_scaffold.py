import os

base_dir = r"c:\Users\deonb\Desktop\GenAI Project\ai-gateway"

files = {
    ".editorconfig": """root = true

[*]
charset = utf-8
end_of_line = lf
indent_size = 4
indent_style = space
insert_final_newline = true
trim_trailing_whitespace = true

[*.{yml,yaml,json,js,ts,md}]
indent_size = 2
""",
    ".pre-commit-config.yaml": """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.272
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
""",
    "Makefile": """install:
\tcd backend && pip install -r requirements.txt
\tcd frontend && npm install

dev:
\tdocker-compose up

docker-up:
\tdocker-compose -f docker-compose.prod.yml up -d

docker-down:
\tdocker-compose down
\tdocker-compose -f docker-compose.prod.yml down

migrate:
\tcd backend && alembic upgrade head

migrate-create:
\tcd backend && alembic revision --autogenerate -m "migration"

lint:
\tcd backend && ruff check .

format:
\tcd backend && black . && isort .

typecheck:
\tcd backend && mypy .

test:
\tcd backend && pytest

clean:
\tfind . -type d -name __pycache__ -exec rm -r {} +
\tfind . -type d -name .pytest_cache -exec rm -r {} +
""",
    "LICENSE": """MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
    "CONTRIBUTING.md": """# Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes using Conventional Commits
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
""",
    "CODE_OF_CONDUCT.md": """# Code of Conduct

Please be respectful to everyone in this community.
""",
    "SECURITY.md": """# Security Policy

## Supported Versions

Only the latest version is supported.

## Reporting a Vulnerability

Please report vulnerabilities by opening a security advisory on GitHub.
""",
    "CHANGELOG.md": """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Initial project foundation.
""",
    "scripts/bootstrap.sh": """#!/bin/bash
echo "Bootstrapping environment..."
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
npm install --prefix frontend
echo "Done."
""",
    "scripts/wait_for_db.sh": """#!/bin/bash
# wait-for-postgres.sh

set -e
host="$1"
shift
cmd="$@"

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
""",
    "scripts/create_admin.py": """import os
import sys

def main():
    print("Creating admin user...")
    # Add real logic later
    print("Admin user created successfully.")

if __name__ == "__main__":
    main()
""",
    "scripts/seed_dev_data.py": """def main():
    print("Seeding development data...")
    # Add seed logic here (no AI data)
    print("Development data seeded.")

if __name__ == "__main__":
    main()
""",
    "scripts/reset_database.py": """def main():
    print("Resetting database...")
    # Add drop/create tables logic here
    print("Database reset complete.")

if __name__ == "__main__":
    main()
""",
    "backend/tests/conftest.py": """import pytest

@pytest.fixture
def db_session():
    # Mock database session
    yield

@pytest.fixture
def redis_client():
    # Mock Redis client
    yield

@pytest.fixture
def authenticated_user():
    return {"id": 1, "username": "testuser"}

@pytest.fixture
def jwt_token():
    return "mock.jwt.token"
""",
    "docker-compose.prod.yml": """version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      - NODE_ENV=production
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: always

  frontend:
    build:
      context: ./frontend
    ports:
      - "3000:3000"
    restart: always

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-admin}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-admin}
      POSTGRES_DB: ${POSTGRES_DB:-ai_gateway}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-admin}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
"""
}

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {full_path}")

# Refactored for performance polish — 2026-05-29T16:25:07
