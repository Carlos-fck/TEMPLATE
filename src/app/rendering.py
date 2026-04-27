"""Template rendering helper.

Centralises the construction of the template context so every page/route
gets the same brand, theme, navigation and user data without repetition.
"""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from typing import Any

from fastapi import Request

from .auth.dependencies import get_current_user
from .config.settings import settings
from .nav import NAV_ITEMS, grouped_items, is_active


def _brand() -> SimpleNamespace:
    return SimpleNamespace(
        name=settings.brand_name,
        short=settings.brand_short,
        logo_url=settings.brand_logo_url,
        tagline=settings.brand_tagline,
    )


def _theme() -> SimpleNamespace:
    return SimpleNamespace(
        primary=settings.theme_primary,
        primary_contrast=settings.theme_primary_contrast,
        secondary=settings.theme_secondary,
        accent=settings.theme_accent,
        bg=settings.theme_bg,
        surface=settings.theme_surface,
        text=settings.theme_text,
        text_muted=settings.theme_text_muted,
        border=settings.theme_border,
        sidebar_bg=settings.theme_sidebar_bg,
        sidebar_text=settings.theme_sidebar_text,
        sidebar_active=settings.theme_sidebar_active,
        danger=settings.theme_danger,
        success=settings.theme_success,
        warning=settings.theme_warning,
        radius=settings.theme_radius,
        font=settings.theme_font,
    )


def _static_url(path: str) -> str:
    return f"/static/{path.lstrip('/')}"


def render(request: Request, template_name: str, /, **context: Any):
    """Render a Jinja template with the standard template globals merged in.

    Pages and partials can rely on these names always being defined:
        request, brand, theme, nav_items, nav_groups, is_active,
        current_path, user, now_year, static_url
    """
    base_ctx: dict[str, Any] = {
        "request": request,
        "brand": _brand(),
        "theme": _theme(),
        "nav_items": NAV_ITEMS,
        "nav_groups": grouped_items(),
        "is_active": is_active,
        "current_path": request.url.path,
        "user": get_current_user(request),
        "now_year": datetime.utcnow().year,
        "static_url": _static_url,
    }
    base_ctx.update(context)
    templates = request.app.state.templates
    status_code = base_ctx.pop("status_code", None)
    kwargs = {"status_code": status_code} if status_code is not None else {}
    return templates.TemplateResponse(request, template_name, base_ctx, **kwargs)
