TEMPLATE - Production-ready Python template

Minimal boilerplate to bootstrap a production-oriented Python service.

Quickstart

1. Create a virtualenv and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the app in development:

```powershell
$env:PYTHONPATH = '.'
uvicorn --factory src.app.factory:create_app --reload --port 8000
```

3. Run tests and linters:

```powershell
$env:PYTHONPATH = '.'
ruff check .
pytest -q
```

Documentation

Extended documentation is in the `docs/` folder. See [docs/README.md](docs/README.md) for details.

