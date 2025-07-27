"""Application settings and configuration management."""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings using Pydantic for validation and environment variable management."""
    
    # Environment settings
    environment: str = Field(default="test", description="Application environment")
    debug: bool = Field(default=False, description="Debug mode")
    
    # OpenWeatherMap API settings
    openweather_api_key: str = Field(..., description="OpenWeatherMap API key")
    openweather_base_url: str = Field(
        default="https://api.openweathermap.org/data/2.5",
        description="OpenWeatherMap API base URL"
    )
    
    # Browser settings
    browser_name: str = Field(default="chromium", description="Browser to use for testing")
    headless: bool = Field(default=True, description="Run browser in headless mode")
    browser_timeout: int = Field(default=30000, description="Browser timeout in milliseconds")
    
    # Test settings
    test_timeout: int = Field(default=30, description="Test timeout in seconds")
    retry_count: int = Field(default=2, description="Number of retries for failed tests")
    
    # UI Test settings
    ui_base_url: str = Field(
        default="https://openweathermap.org",
        description="Base URL for UI testing"
    )
    
    # Screenshot and video settings
    screenshot_mode: str = Field(default="only-on-failure", description="Screenshot capture mode")
    video_mode: str = Field(default="retain-on-failure", description="Video capture mode")
    
    # Reporting settings
    allure_results_dir: str = Field(default="reports/allure-results", description="Allure results directory")
    html_report_dir: str = Field(default="reports/html", description="HTML report directory")
    
    # Performance settings
    performance_threshold_ms: int = Field(
        default=2000,
        description="Performance threshold in milliseconds"
    )
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings 