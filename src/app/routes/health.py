from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from ..cache import get_redis
from ..db.engine import engine

router = APIRouter()


@router.get("/health")
async def health():
    """Liveness probe — process is up. Use this for the platform healthcheck."""
    return {"status": "ok"}


@router.get("/live")
async def live():
    return {"status": "live"}


@router.get("/ready")
async def ready():
    """Readiness probe — DB and Redis are reachable.

    Returns 503 when a dependency is down so Coolify / load balancers can
    drain traffic until the app recovers.
    """
    checks: dict[str, str] = {}
    ok = True

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as exc:  # noqa: BLE001 - surface root cause briefly
        checks["database"] = f"error: {exc.__class__.__name__}"
        ok = False

    try:
        get_redis().ping()
        checks["redis"] = "ok"
    except Exception as exc:  # noqa: BLE001
        checks["redis"] = f"error: {exc.__class__.__name__}"
        ok = False

    payload = {"status": "ready" if ok else "degraded", "checks": checks}
    return JSONResponse(payload, status_code=200 if ok else 503)
