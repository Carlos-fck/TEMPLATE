"""Authentication module — session-based login for the template."""

from .dependencies import (
    get_current_user,
    require_user,
    require_user_redirect,
)

__all__ = ["get_current_user", "require_user", "require_user_redirect"]
