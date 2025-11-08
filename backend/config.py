"""
Configuration management for Solar PV Lab OS
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""

    # AI Configuration
    anthropic_api_key: str = ""
    ai_model: str = "claude-3-5-sonnet-20241022"
    ai_max_tokens: int = 4096

    # Application
    app_name: str = "Solar PV Lab OS - AI Report Generator"
    app_version: str = "1.0.0"
    debug: bool = True

    # Paths
    reports_output_dir: str = "./sample_data/generated_reports"
    templates_dir: str = "./templates/report_templates"
    max_report_size_mb: int = 50

    # Lab Information
    lab_name: str = "Solar PV Testing Laboratory"
    lab_nabl_cert: str = "TC-XXXX"
    lab_address: str = "Your Lab Address"
    lab_phone: str = "+91-XXXXXXXXXX"
    lab_email: str = "lab@example.com"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Ensure output directories exist
def setup_directories():
    """Create necessary directories"""
    settings = get_settings()
    Path(settings.reports_output_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.templates_dir).mkdir(parents=True, exist_ok=True)
