# Deployment

Docker image build

```bash
docker build -t template:latest .
```

Run container (example)

```bash
docker run --rm -p 8000:8000 \
  -e DATABASE_URL='postgresql+psycopg://user:pass@host:5432/db' \
  -e REDIS_URL='redis://host:6379/0' \
  template:latest
```

Docker Compose

```bash
docker compose up -d --build
```

Coolify / PaaS notes
- Ensure environment variables/secrets are configured in the target platform.
- For Coolify, adapt the `docker-compose.yml` service definitions to match platform expectations and set health checks and exposed ports accordingly.

Security
- Do not commit real secrets; use `.env` for local development and platform secrets for production.
