#!/usr/bin/env bash
# =============================================================================
# Container entrypoint.
#   * Waits for Postgres (when DATABASE_URL points to a TCP host).
#   * Runs Alembic migrations only when RUN_MIGRATIONS=1 (the worker container
#     should set RUN_MIGRATIONS=0 to avoid races during scale-out).
# =============================================================================
set -euo pipefail

log() { printf '[entrypoint] %s\n' "$*"; }

RUN_MIGRATIONS="${RUN_MIGRATIONS:-0}"
POSTGRES_HOST="${POSTGRES_HOST:-db}"
POSTGRES_PORT="${POSTGRES_PORT:-5432}"
POSTGRES_USER="${POSTGRES_USER:-postgres}"
POSTGRES_WAIT_TIMEOUT="${POSTGRES_WAIT_TIMEOUT:-60}"

wait_for_postgres() {
  command -v pg_isready >/dev/null 2>&1 || return 0
  log "waiting for Postgres at ${POSTGRES_HOST}:${POSTGRES_PORT} (timeout ${POSTGRES_WAIT_TIMEOUT}s)"
  local i=0
  while ! pg_isready -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}" -q; do
    i=$((i + 1))
    if [ "$i" -ge "${POSTGRES_WAIT_TIMEOUT}" ]; then
      log "Postgres not ready after ${POSTGRES_WAIT_TIMEOUT}s, continuing anyway"
      return 0
    fi
    sleep 1
  done
  log "Postgres is ready"
}

run_migrations() {
  if [ "${RUN_MIGRATIONS}" != "1" ]; then
    log "RUN_MIGRATIONS=${RUN_MIGRATIONS}, skipping alembic"
    return 0
  fi
  if ! command -v alembic >/dev/null 2>&1; then
    log "alembic binary not found, skipping migrations"
    return 0
  fi
  log "running alembic upgrade head"
  alembic upgrade head
}

wait_for_postgres
run_migrations

log "exec: $*"
exec "$@"
