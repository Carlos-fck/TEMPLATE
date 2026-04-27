.PHONY: dev test lint format migrate worker up down build logs ps shell

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
	celery -A src.app.celery_app.celery_app worker --loglevel=info

build:
	docker compose build

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

shell:
	docker compose exec app bash
