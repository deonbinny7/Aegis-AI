install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

dev:
	docker-compose up

docker-up:
	docker-compose -f docker-compose.prod.yml up -d

docker-down:
	docker-compose down
	docker-compose -f docker-compose.prod.yml down

migrate:
	cd backend && alembic upgrade head

migrate-create:
	cd backend && alembic revision --autogenerate -m "migration"

lint:
	cd backend && ruff check .

format:
	cd backend && black . && isort .

typecheck:
	cd backend && mypy .

test:
	cd backend && pytest

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type d -name .pytest_cache -exec rm -r {} +
