"""Deprecated — kept for backwards compatibility.

The dashboard / index page now lives in :mod:`src.app.routes.pages`. This
module is no longer registered in :func:`src.app.factory.create_app`.
"""

from fastapi import APIRouter

router = APIRouter()
