# syntax=docker/dockerfile:1.7
# =============================================================================
# Multi-stage build optimised for VPS / Coolify deployments.
# Stage 1: build wheels into an isolated venv at /opt/venv.
# Stage 2: slim runtime image with only the venv + app + curl (healthchecks).
# =============================================================================

FROM python:3.14-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip

COPY requirements.txt ./
RUN /opt/venv/bin/pip install -r requirements.txt


FROM python:3.14-slim AS runtime

ARG APP_USER=template
ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:${PATH}" \
    PYTHONPATH=/app

WORKDIR /app

# curl: app & worker healthchecks. libpq5: psycopg runtime dep.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -g ${APP_GID} ${APP_USER} \
    && useradd -m -u ${APP_UID} -g ${APP_GID} -s /usr/sbin/nologin ${APP_USER}

COPY --from=builder /opt/venv /opt/venv
COPY --chown=${APP_USER}:${APP_USER} . /app

RUN chmod +x /app/scripts/docker-entrypoint.sh

USER ${APP_USER}

EXPOSE 8000

# Container-level healthcheck (used when running `docker run` directly; Compose
# overrides this with its own `healthcheck` blocks).
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=5 \
  CMD curl -fsS http://localhost:8000/health || exit 1

ENTRYPOINT ["/app/scripts/docker-entrypoint.sh"]
CMD ["uvicorn", "--factory", "src.app.factory:create_app", "--host", "0.0.0.0", "--port", "8000"]
