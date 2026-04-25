.PHONY: dev test lint format migrate worker up down

dev:
	uvicorn --factory src.app.factory:create_app --reload

test:
	pytest -q

lint:
	ruff check .

format:
	ruff format .

migrate:
	./scripts/migrate.sh

worker:
	celery -A src.app.worker.app worker --loglevel=info

up:
	docker-compose up -d --build

down:
	docker-compose down
