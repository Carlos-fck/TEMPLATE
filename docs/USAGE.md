# Quick Usage / Getting Started

Requirements
- Python 3.14+
- Docker (optional)

Local development (PowerShell example)

```powershell
cd C:\Projetos-Git\TEMPLATE
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
$env:PYTHONPATH = '.'
uvicorn --factory src.app.factory:create_app --reload --port 8000
```

Run tests and linters

```powershell
$env:PYTHONPATH = '.'
ruff check .
pytest -q
```

Database migrations

- Configure `DATABASE_URL` in environment or `.env` and run:

```bash
./scripts/migrate.sh
# or
alembic upgrade head
```

Docker (Compose)

```bash
docker compose up -d --build
# open http://localhost:8000
```

Notes
- Example `.env` available at `.env.example`.
- On Windows, set `PYTHONPATH` before running tests so tests can import `src`.
