#!/usr/bin/env bash
set -euo pipefail

echo "[entrypoint] starting: $*"

# Wait for Postgres to be ready (if pg_isready is available)
if command -v pg_isready >/dev/null 2>&1; then
  echo "[entrypoint] waiting for Postgres..."
  for i in $(seq 1 30); do
    pg_isready -h "${POSTGRES_HOST:-db}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-postgres}" && break
    echo "[entrypoint] Postgres not ready ($i/30)"
    sleep 1
  done
fi

# Run Alembic migrations if available
if command -v alembic >/dev/null 2>&1; then
  echo "[entrypoint] running alembic migrations"
  alembic upgrade head || echo "[entrypoint] alembic upgrade failed, continuing"
else
  echo "[entrypoint] alembic not found, skipping migrations"
fi

exec "$@"
