"""FastAPI dependencies for authentication."""

from __future__ import annotations

from typing import Optional
from urllib.parse import quote

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException

from .users import User, get_user


SESSION_USER_KEY = "user"


def _session_username(request: Request) -> Optional[str]:
    session = getattr(request, "session", None)
    if not session:
        return None
    return session.get(SESSION_USER_KEY)


def get_current_user(request: Request) -> Optional[User]:
    """Return the authenticated user or ``None``. Never raises."""
    username = _session_username(request)
    if not username:
        return None
    return get_user(username)


def require_user(request: Request) -> User:
    """Dependency that raises 401 if the user isn't authenticated.

    Use for JSON/API endpoints.
    """
    user = get_current_user(request)
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


def require_user_redirect(request: Request) -> User:
    """Dependency for HTML pages — redirects to /login when unauthenticated."""
    user = get_current_user(request)
    if user is None:
        next_url = quote(str(request.url.path))
        # Raising HTTPException with a Location header is awkward; use a
        # custom exception class handled at app level instead.
        raise _RedirectToLogin(next_url)
    return user


class _RedirectToLogin(Exception):
    def __init__(self, next_url: str) -> None:
        self.next_url = next_url


def install_redirect_handler(app) -> None:
    """Register the exception handler that converts auth redirects."""
    @app.exception_handler(_RedirectToLogin)
    async def _handler(_request: Request, exc: _RedirectToLogin):
        return RedirectResponse(url=f"/login?next={exc.next_url}", status_code=303)


def login_session(request: Request, user: User) -> None:
    request.session[SESSION_USER_KEY] = user.username


def logout_session(request: Request) -> None:
    request.session.pop(SESSION_USER_KEY, None)
