from pathlib import Path
import uuid
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from .routes.root import router as root_router
from .routes.health import router as health_router
from .logging_config import configure_logging


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    configure_logging()
    app = FastAPI(title="TEMPLATE")
    templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
    app.state.templates = templates

    @app.middleware("http")
    async def add_correlation_id(request: Request, call_next):
        cid = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
        request.state.correlation_id = cid
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = cid
        return response

    app.include_router(root_router)
    app.include_router(health_router)
    return app
