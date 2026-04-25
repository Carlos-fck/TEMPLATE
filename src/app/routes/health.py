from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/ready")
async def ready():
    # simple readiness probe; extend with DB/Redis checks
    return {"status": "ready"}


@router.get("/live")
async def live():
    return {"status": "live"}
