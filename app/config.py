"""
config.py — Environment variable loading and application settings.

Reads from the .env file using pydantic-settings.
Sanitizes secrets so they are never accidentally logged or exposed.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    All configuration values are loaded from environment variables or the .env file.
    Defaults are provided for non-secret values.
    """

    # ── Groq API ──────────────────────────────────────────────
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    groq_model: str = Field(default="openai/gpt-oss-120b", alias="GROQ_MODEL")

    # ── Server ────────────────────────────────────────────────
    host: str = Field(default="127.0.0.1", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    # ── Agent behaviour ───────────────────────────────────────
    request_timeout: int = Field(default=60, alias="REQUEST_TIMEOUT")

    # ── App metadata ──────────────────────────────────────────
    app_name: str = "LegalBot — Multi-Agent Legal Assistant"
    app_version: str = "1.0.0"

    class Config:
        env_file = ".env"           # load from .env in working directory
        env_file_encoding = "utf-8"
        populate_by_name = True     # allow both alias and field name

    # ── Helper properties ─────────────────────────────────────

    @property
    def groq_configured(self) -> bool:
        """True when a non-empty API key is present."""
        return bool(self.groq_api_key and self.groq_api_key.strip())

    @property
    def masked_api_key(self) -> str:
        """
        Returns a masked version of the API key safe for logging.
        Example: gsk_z9zE...x6Y8
        """
        key = self.groq_api_key
        if not key or len(key) < 12:
            return "NOT_SET"
        return f"{key[:8]}...{key[-4:]}"

    def __repr__(self) -> str:
        # Never print the real key in repr / logs
        return (
            f"Settings(app_name={self.app_name!r}, "
            f"groq_model={self.groq_model!r}, "
            f"groq_configured={self.groq_configured}, "
            f"host={self.host!r}, port={self.port})"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Returns a cached singleton Settings instance.
    Using lru_cache means .env is only parsed once per process.
    """
    return Settings()
