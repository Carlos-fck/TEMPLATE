"""Protected HTML pages — example pages rendered behind the login wall."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from ..auth.dependencies import require_user_redirect
from ..auth.users import User
from ..rendering import render

router = APIRouter()


@router.get("/", name="dashboard")
async def dashboard(request: Request, user: User = Depends(require_user_redirect)):
    return render(request, "pages/dashboard.html", page_title="Dashboard")


@router.get("/profile", name="profile")
async def profile(request: Request, user: User = Depends(require_user_redirect)):
    return render(request, "pages/profile.html", page_title="Profile")


@router.get("/settings", name="settings")
async def settings_page(request: Request, user: User = Depends(require_user_redirect)):
    return render(request, "pages/settings.html", page_title="Settings")
