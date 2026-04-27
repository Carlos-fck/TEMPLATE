# Deployment

This template is built to run on a Linux VPS via Docker Compose. The default
[docker-compose.yml](../docker-compose.yml) is the same file Coolify reads when
you point it at the repo.

---

## 1. What ships in the image

- `Dockerfile` — multi-stage build with a private virtualenv at `/opt/venv`,
  non-root `template` user, container-level `HEALTHCHECK` against `/health`.
- `scripts/docker-entrypoint.sh` — waits for Postgres, runs Alembic migrations
  when `RUN_MIGRATIONS=1`, then `exec`s the container command.
- `.dockerignore` — keeps the build context small (no `.venv`, no `tests/`,
  no `docs/`).

Build locally:

```bash
docker build -t template:latest .
```

Run a single container against external services:

```bash
docker run --rm -p 8000:8000 \
  -e ENV=production \
  -e SECRET_KEY="$(openssl rand -hex 32)" \
  -e DATABASE_URL="postgresql+psycopg://user:pass@host:5432/db" \
  -e REDIS_URL="redis://host:6379/0" \
  -e CELERY_BROKER_URL="redis://host:6379/1" \
  -e RUN_MIGRATIONS=1 \
  template:latest
```

---

## 2. Compose stack (VPS)

```bash
cp .env.example .env
# edit .env (at minimum: SECRET_KEY, ADMIN_PASSWORD, POSTGRES_PASSWORD)
docker compose up -d --build
docker compose logs -f app
```

Services:

| Service | Public port | Notes |
|---|---|---|
| `app`    | `${APP_PORT}` (default 8000) | FastAPI + Uvicorn. Runs migrations on boot. |
| `worker` | —                            | Celery worker. `RUN_MIGRATIONS=0`. |
| `db`     | —                            | Postgres 17. Internal only. Volume `pgdata`. |
| `redis`  | —                            | Redis 7. Internal only. Volume `redis_data`. |

Only `app` publishes a host port. `db` and `redis` are reachable through the
internal `template_internal` network and are never exposed publicly.

`depends_on` uses `condition: service_healthy`, so app/worker only start once
Postgres and Redis answer their healthchecks.

---

## 3. Coolify deployment

Coolify supports the bundled Compose file directly.

### 3.1 Create the application

1. **+ New Resource → Docker Compose** (or **Public Repository** if pulling
   from Git).
2. Paste / import the [docker-compose.yml](../docker-compose.yml).
3. Coolify auto-detects the `app` service as the public one (the only one with
   a published port).

### 3.2 Required environment variables

Set these in the Coolify panel — they are read by the `app` and `worker`
services through `env_file: .env` (Coolify generates the `.env` for you):

```ini
ENV=production
SECRET_KEY=<generate with: openssl rand -hex 32>

DATABASE_URL=postgresql+psycopg://postgres:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1

POSTGRES_USER=postgres
POSTGRES_PASSWORD=<strong-random>
POSTGRES_DB=template_db

# Branding / theme — override per project
BRAND_NAME=My Project
BRAND_TAGLINE=Internal tools
THEME_PRIMARY=#7c3aed

# Auth seed — replace before exposing publicly
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<strong-random>
```

`create_app()` will hard-fail at boot if `ENV=production` and
`SECRET_KEY`/`ADMIN_PASSWORD` are still defaults.

### 3.3 Domain & TLS

In Coolify:

- Set the **Domain** on the `app` service (e.g. `app.example.com`).
- Coolify provisions Let's Encrypt automatically and routes traffic to
  container port `8000`.
- Because `ENV=production`, the session cookie is sent with `Secure` so
  HTTPS is required.

### 3.4 Healthchecks

- Liveness: `GET /health` (used by the container `HEALTHCHECK`).
- Readiness: `GET /ready` — pings Postgres and Redis, returns `503` when a
  dependency is down. Configure Coolify's "Healthcheck Path" to `/ready` if
  you want the proxy to drain traffic during incidents.

### 3.5 Persistent storage

The Compose file declares two named volumes managed by Coolify:

- `pgdata` → Postgres data
- `redis_data` → Redis AOF/RDB snapshots

Configure backups in Coolify → **Storage** for both volumes.

### 3.6 Scaling

- **Worker**: increase `CELERY_CONCURRENCY` in `.env`, or scale the `worker`
  service replicas in Coolify. Migrations are *not* re-run because
  `RUN_MIGRATIONS=0` for the worker.
- **App**: scaling the `app` service horizontally is safe; only one instance
  needs to run migrations at boot. If you scale beyond 1 instance you should
  either run migrations as a separate one-shot step (Coolify "Pre-deploy
  command": `alembic upgrade head`) and set `RUN_MIGRATIONS=0` on `app`.

---

## 4. Updates / rollbacks

Coolify rebuilds on every push to the configured branch. To deploy manually:

```bash
git pull
docker compose pull           # if using a registry image
docker compose up -d --build
```

Rollback by redeploying a previous Git commit (Coolify keeps deployment
history) or by `docker compose up -d --image template:<previous-tag>`.

---

## 5. Security checklist

- [ ] `ENV=production`
- [ ] `SECRET_KEY` is unique and random (≥32 bytes)
- [ ] `POSTGRES_PASSWORD` and `ADMIN_PASSWORD` rotated from defaults
- [ ] Domain has TLS (Coolify Let's Encrypt enabled)
- [ ] Postgres/Redis ports are NOT published to the host (default in this
      compose file — do not add `ports:` blocks to those services)
- [ ] Backups configured for the `pgdata` volume
- [ ] `BRAND_LOGO_URL` (if external) is served over HTTPS
