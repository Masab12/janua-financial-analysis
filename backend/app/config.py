"""
Configuration settings for the JANUA Financial Analysis API.
Keeps all the important settings in one place instead of scattered everywhere.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    If you need to change something, create a .env file in the backend folder.
    """
    
    # API Settings
    app_name: str = "JANUA Financial Analysis API"
    app_version: str = "1.0.0"
    api_prefix: str = "/api"
    
    # CORS - Which websites can call our API
    # For production, replace localhost with actual domains
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://janua.pt",
        "https://www.janua.pt",
    ]
    
    # Calculation Settings
    trend_threshold: float = 0.05  # 5% change triggers trend arrow
    
    # Logging
    log_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    log_file: str = "logs/api.log"
    
    # Validation Thresholds
    # These prevent obviously wrong data from being processed
    max_financial_value: float = 1_000_000_000_000  # 1 trillion (sanity check)
    min_years_required: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create a single instance to use throughout the app
settings = Settings()
