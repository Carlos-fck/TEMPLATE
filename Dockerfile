FROM python:3.14-slim AS builder

WORKDIR /app

COPY requirements.txt ./

# Install build deps and build wheels into /install to copy into final image
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl passwd \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install --no-cache-dir --target=/install -r requirements.txt

FROM python:3.14-slim AS runtime

ARG APP_USER=template
ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /install

# Copy application
COPY . /app

# Ensure a non-root user exists and chown app dir
RUN groupadd -g ${APP_GID} ${APP_USER} || true \
    && useradd -m -u ${APP_UID} -g ${APP_GID} -s /bin/bash ${APP_USER} || true \
    && chown -R ${APP_USER}:${APP_USER} /app

# Make entrypoint executable and ensure curl exists for healthchecks
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && chmod +x /app/scripts/docker-entrypoint.sh

ENV PYTHONPATH=/install:${PYTHONPATH}

# Run containers as non-root user by default
USER ${APP_USER}

ENV PATH="/home/${APP_USER}/.local/bin:${PATH}"

ENTRYPOINT ["/app/scripts/docker-entrypoint.sh"]
CMD ["python", "-m", "uvicorn", "--factory", "src.app.factory:create_app", "--host", "0.0.0.0", "--port", "8000"]
