"""Auth HTTP routes — login form, login submit, logout."""

from __future__ import annotations

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse

from ..auth.dependencies import login_session, logout_session
from ..auth.users import authenticate
from ..rendering import render

router = APIRouter()


@router.get("/login", name="login")
async def login_form(request: Request, next: str = "/"):
    return render(
        request,
        "auth/login.html",
        next=next,
        error=None,
        username="",
    )


@router.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    next: str = Form("/"),
):
    user = authenticate(username, password)
    if user is None:
        return render(
            request,
            "auth/login.html",
            next=next,
            error="Credenciais inválidas.",
            username=username,
            status_code=401,
        )
    login_session(request, user)
    safe_next = next if next.startswith("/") and not next.startswith("//") else "/"
    return RedirectResponse(url=safe_next, status_code=303)


@router.post("/logout", name="logout")
@router.get("/logout")
async def logout(request: Request):
    logout_session(request)
    return RedirectResponse(url="/login", status_code=303)
