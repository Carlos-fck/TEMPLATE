try:
    # Prefer the standalone pydantic-settings package (Pydantic v2+)
    from pydantic_settings import BaseSettings as _BaseSettings  # type: ignore
    PYDANTIC_SETTINGS = True
except Exception:
    # Fallback to the legacy location (pydantic.BaseSettings)
    from pydantic import BaseSettings as _BaseSettings  # type: ignore
    PYDANTIC_SETTINGS = False

from pydantic import Field


class _BaseTemplateSettings(_BaseSettings):  # type: ignore[misc, valid-type]
    # Core
    env: str = Field("development", env="ENV")
    database_url: str = Field(
        "postgresql+psycopg://postgres:postgres@db:5432/template_db",
        env="DATABASE_URL",
    )
    redis_url: str = Field("redis://redis:6379/0", env="REDIS_URL")
    celery_broker_url: str = Field("redis://redis:6379/1", env="CELERY_BROKER_URL")
    secret_key: str = Field("changeme", env="SECRET_KEY")

    # Session / auth -------------------------------------------------------
    session_cookie: str = Field("template_session", env="SESSION_COOKIE")
    session_max_age: int = Field(60 * 60 * 8, env="SESSION_MAX_AGE")  # 8h
    # Demo credentials so the template is usable out-of-the-box.
    # Replace with a real user store (DB) in your application.
    admin_username: str = Field("admin", env="ADMIN_USERNAME")
    admin_password: str = Field("admin", env="ADMIN_PASSWORD")

    # Branding -------------------------------------------------------------
    brand_name: str = Field("TEMPLATE", env="BRAND_NAME")
    brand_short: str = Field("T", env="BRAND_SHORT")
    brand_logo_url: str = Field("", env="BRAND_LOGO_URL")
    brand_tagline: str = Field("Production-ready boilerplate", env="BRAND_TAGLINE")

    # Theme — any valid CSS color value -----------------------------------
    theme_primary: str = Field("#2563eb", env="THEME_PRIMARY")
    theme_primary_contrast: str = Field("#ffffff", env="THEME_PRIMARY_CONTRAST")
    theme_secondary: str = Field("#64748b", env="THEME_SECONDARY")
    theme_accent: str = Field("#10b981", env="THEME_ACCENT")
    theme_bg: str = Field("#f8fafc", env="THEME_BG")
    theme_surface: str = Field("#ffffff", env="THEME_SURFACE")
    theme_text: str = Field("#0f172a", env="THEME_TEXT")
    theme_text_muted: str = Field("#64748b", env="THEME_TEXT_MUTED")
    theme_border: str = Field("#e2e8f0", env="THEME_BORDER")
    theme_sidebar_bg: str = Field("#0f172a", env="THEME_SIDEBAR_BG")
    theme_sidebar_text: str = Field("#e2e8f0", env="THEME_SIDEBAR_TEXT")
    theme_sidebar_active: str = Field("#1e293b", env="THEME_SIDEBAR_ACTIVE")
    theme_danger: str = Field("#ef4444", env="THEME_DANGER")
    theme_success: str = Field("#22c55e", env="THEME_SUCCESS")
    theme_warning: str = Field("#f59e0b", env="THEME_WARNING")
    theme_radius: str = Field("8px", env="THEME_RADIUS")
    theme_font: str = Field(
        "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif",
        env="THEME_FONT",
    )


if PYDANTIC_SETTINGS:
    class Settings(_BaseTemplateSettings):
        model_config = {
            "env_file": ".env",
            "env_file_encoding": "utf-8",
            "extra": "ignore",
        }

else:
    class Settings(_BaseTemplateSettings):
        class Config:  # type: ignore
            env_file = ".env"
            env_file_encoding = "utf-8"
            extra = "ignore"


settings = Settings()
