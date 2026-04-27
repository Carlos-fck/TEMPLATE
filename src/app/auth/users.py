"""In-memory user store.

Replace this module with a database-backed implementation in your
application. The interface (`get_user`, `authenticate`) is intentionally
small so it can be swapped without touching routes or templates.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..config.settings import settings
from .security import hash_password, verify_password


@dataclass(frozen=True)
class User:
    username: str
    display_name: str
    email: str = ""
    is_admin: bool = False


# --- in-memory store ---------------------------------------------------------
_USERS: dict[str, dict] = {}


def _bootstrap() -> None:
    """Seed the default admin user from environment settings."""
    if settings.admin_username and settings.admin_password:
        _USERS[settings.admin_username] = {
            "user": User(
                username=settings.admin_username,
                display_name=settings.admin_username.title(),
                email=f"{settings.admin_username}@example.com",
                is_admin=True,
            ),
            "password_hash": hash_password(settings.admin_password),
        }


_bootstrap()


def get_user(username: str) -> Optional[User]:
    record = _USERS.get(username)
    return record["user"] if record else None


def authenticate(username: str, password: str) -> Optional[User]:
    record = _USERS.get(username)
    if not record:
        return None
    if not verify_password(password, record["password_hash"]):
        return None
    return record["user"]
