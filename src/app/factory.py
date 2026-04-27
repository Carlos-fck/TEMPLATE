from pathlib import Path
import uuid

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from .auth.dependencies import install_redirect_handler
from .auth.routes import router as auth_router
from .config.settings import settings
from .logging_config import configure_logging
from .routes.health import router as health_router
from .routes.pages import router as pages_router


_WEAK_SECRETS = {"", "changeme", "change-me", "secret"}


def _validate_production_settings() -> None:
    """Hard-fail on insecure defaults when running in production.

    Coolify deployments set ENV=production via the panel; this guard catches
    forgotten secrets early instead of silently shipping them.
    """
    if settings.env not in {"production", "prod"}:
        return
    if settings.secret_key in _WEAK_SECRETS:
        raise RuntimeError(
            "SECRET_KEY must be set to a strong, unique value when ENV=production."
        )
    if (
        settings.admin_password in {"admin", "changeme", "change-me", ""}
        and settings.admin_username == "admin"
    ):
        raise RuntimeError(
            "Default admin credentials detected. Set ADMIN_USERNAME/ADMIN_PASSWORD "
            "(or remove the seed) before running in production."
        )


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    configure_logging()
    _validate_production_settings()
    app = FastAPI(title=settings.brand_name)

    base_dir = Path(__file__).parent
    templates = Jinja2Templates(directory=str(base_dir / "templates"))
    app.state.templates = templates

    # Middleware: session + correlation id
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.secret_key,
        session_cookie=settings.session_cookie,
        max_age=settings.session_max_age,
        same_site="lax",
        https_only=settings.env in {"production", "prod"},
    )

    @app.middleware("http")
    async def add_correlation_id(request: Request, call_next):
        cid = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
        request.state.correlation_id = cid
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = cid
        return response

    # Static assets
    static_dir = base_dir / "static"
    static_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # Routers + exception handlers
    install_redirect_handler(app)
    app.include_router(auth_router)
    app.include_router(health_router)
    app.include_router(pages_router)
    return app
