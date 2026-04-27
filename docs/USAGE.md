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

---

## Web UI included

The template ships with a generic, themeable web UI:

- **Login page** at `/login` (default credentials from `.env`: `ADMIN_USERNAME` / `ADMIN_PASSWORD`).
- **Protected pages**: `/` (dashboard), `/profile`, `/settings`. Unauthenticated users are redirected to `/login`.
- **Sidebar** with brand area (logo + name + tagline) and grouped, data-driven nav.
- **Topbar** with user avatar and a sidebar toggle for small screens.
- **Themable** via CSS variables — change `THEME_*` in `.env` to recolor the entire app.

### Customise branding & theme

Edit `.env`:

```
BRAND_NAME=My Project
BRAND_SHORT=MP
BRAND_LOGO_URL=/static/img/logo.svg     # optional
BRAND_TAGLINE=Internal tools

THEME_PRIMARY=#7c3aed
THEME_SIDEBAR_BG=#1e1b4b
THEME_RADIUS=12px
```

### Add a sidebar item

Edit [src/app/nav.py](src/app/nav.py):

```python
NAV_ITEMS.append({
    "label": "Reports",
    "url": "/reports",
    "icon": "home",
    "section": "Main",
    "match": ["/reports"],
})
```

### Add a new protected page

1. Create a Jinja template under `src/app/templates/pages/`, e.g. `reports.html`:

   ```jinja
   {% extends "layouts/app.html" %}
   {% block content %}<p>Hello reports.</p>{% endblock %}
   ```

2. Register a route in [src/app/routes/pages.py](src/app/routes/pages.py):

   ```python
   from ..auth.dependencies import require_user_redirect
   from ..rendering import render

   @router.get("/reports")
   async def reports(request: Request, user=Depends(require_user_redirect)):
       return render(request, "pages/reports.html", page_title="Reports")
   ```

### Template structure (Jinja modularization)

```
templates/
├── base.html                 # HTML skeleton + theme inject
├── layouts/
│   ├── app.html              # sidebar + topbar + content
│   └── auth.html             # centered card (login/signup)
├── partials/
│   ├── theme.css.html        # CSS variables from settings
│   ├── brand_logo.html
│   ├── sidebar.html
│   ├── sidebar_brand.html
│   ├── sidebar_nav.html
│   ├── icon.html
│   ├── topbar.html
│   ├── flash.html
│   ├── footer.html
│   └── card.html
├── auth/
│   └── login.html
└── pages/
    ├── dashboard.html
    ├── profile.html
    └── settings.html
```

Pages should always extend a layout (`layouts/app.html` or `layouts/auth.html`),
never `base.html` directly. Override one specific partial in your project to
re-skin a single area without touching the others.
