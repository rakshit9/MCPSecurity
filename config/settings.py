from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """MCPSecurity Gateway Configuration"""
    OPENAI_API_KEY: str = "sk-placeholder-key-not-set"
    OPENAI_MODEL: str = "gpt-4"
    MCP_SERVER_HOST: str = "0.0.0.0"
    MCP_SERVER_PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True
        
    def is_configured(self) -> bool:
        """Check if API key is properly configured"""
        return self.OPENAI_API_KEY != "sk-placeholder-key-not-set" and \
               not self.OPENAI_API_KEY.startswith("your_")


settings = Settings()

if not settings.is_configured() and settings.ENVIRONMENT != "development":
    import warnings
    warnings.warn(
        "OPENAI_API_KEY is not configured. Please set it in .env file. "
        "Copy .env.example to .env and add your API key."
    )

