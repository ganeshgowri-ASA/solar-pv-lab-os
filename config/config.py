"""
Configuration Management for Solar PV Lab OS
"""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # Anthropic API
    anthropic_api_key: str = ""

    # AI Configuration
    ai_model: str = "claude-sonnet-4-5-20250929"
    ai_max_tokens: int = 4096
    ai_temperature: float = 0.7

    # Session Configuration
    session_timeout: int = 3600
    max_context_messages: int = 10

    # Database
    database_url: str = "sqlite:///./solar_pv_lab.db"

    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"

    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8501"
    ]

    class Config:
        env_file = ".env"
        case_sensitive = False


# Singleton instance
_settings_instance = None


def get_settings() -> Settings:
    """Get application settings singleton"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
