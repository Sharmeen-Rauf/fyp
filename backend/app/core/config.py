"""
Application Configuration
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Botboss"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]
    
    # Database
    DATABASE_URL: str = "sqlite:///./botboss.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    
    # Twilio
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_API_KEY: str = ""
    TWILIO_API_SECRET: str = ""
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

