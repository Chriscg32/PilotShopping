from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings with Hugging Face integration."""
    
    # Application
    APP_NAME: str = Field(default="Multi-Agent System with Hugging Face")
    VERSION: str = Field(default="0.3.0")
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    
    # API Configuration
    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)
    API_PREFIX: str = Field(default="/api/v1")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: str = Field(default="logs/app.log")
    
    # Hugging Face Configuration
    HUGGINGFACE_API_KEY: str = Field(default="", description="Hugging Face API key")
    HUGGINGFACE_API_URL: str = Field(default="https://api-inference.huggingface.co/models")
    HUGGINGFACE_TIMEOUT: int = Field(default=30)
    
    # Default Models
    DEFAULT_TEXT_MODEL: str = Field(default="microsoft/DialoGPT-medium")
    DEFAULT_SENTIMENT_MODEL: str = Field(default="cardiffnlp/twitter-roberta-base-sentiment-latest")
    DEFAULT_CODE_MODEL: str = Field(default="microsoft/CodeBERT-base")
    DEFAULT_MARKETING_MODEL: str = Field(default="gpt2")
    
    # Model Configuration
    MAX_TOKENS: int = Field(default=512)
    TEMPERATURE: float = Field(default=0.7)
    TOP_P: float = Field(default=0.9)
    FREQUENCY_PENALTY: float = Field(default=0.0)
    PRESENCE_PENALTY: float = Field(default=0.0)
    
    # Agent Configuration
    AGENT_TIMEOUT: int = Field(default=60)
    MAX_CONCURRENT_TASKS: int = Field(default=10)
    TASK_RETRY_ATTEMPTS: int = Field(default=3)
    
    # Database
    DATABASE_URL: str = Field(default="sqlite:///./data/agents.db")
    DATABASE_ECHO: bool = Field(default=False)
    
    # Redis
    REDIS_URL: Optional[str] = Field(default=None)
    REDIS_TIMEOUT: int = Field(default=5)
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    ALGORITHM: str = Field(default="HS256")
    
    # File Storage
    UPLOAD_DIR: str = Field(default="./uploads")
    MAX_FILE_SIZE: int = Field(default=10485760)  # 10MB
    ALLOWED_EXTENSIONS: List[str] = Field(default=[".txt", ".md", ".py", ".js", ".html", ".css", ".json", ".yaml", ".yml"])
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100)
    RATE_LIMIT_WINDOW: int = Field(default=3600)  # 1 hour
    
    # CORS
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000", "http://localhost:8080"])
    
    @validator("HUGGINGFACE_API_KEY")
    def validate_huggingface_key(cls, v):
        if not v and os.getenv("ENVIRONMENT", "development") == "production":
            raise ValueError("Hugging Face API key is required in production")
        return v
    
    @validator("LOG_FILE")
    def create_log_directory(cls, v):
        log_path = Path(v)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        return v
    
    @validator("UPLOAD_DIR")
    def create_upload_directory(cls, v):
        Path(v).mkdir(parents=True, exist_ok=True)
        return v
    
    @validator("DATABASE_URL")
    def create_data_directory(cls, v):
        if v.startswith("sqlite"):
            db_path = Path(v.replace("sqlite:///", ""))
            db_path.parent.mkdir(parents=True, exist_ok=True)
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
_settings = None

def get_settings() -> Settings:
    """Get application settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings