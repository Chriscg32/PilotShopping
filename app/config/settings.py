import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    # App Configuration
    app_name: str = "Landing Copy Generator"
    app_version: str = "0.3.0"
    debug: bool = False
    
    # API Configuration
    api_v1_prefix: str = "/api/v1"
    host: str = "127.0.0.1"
    port: int = 8000
    
    # Environment
    environment: str = "development"
    
    # MQTT Configuration
    mqtt_broker_host: Optional[str] = None
    mqtt_broker_port: int = 1883
    mqtt_username: Optional[str] = None
    mqtt_password: Optional[str] = None
    
    # External API Keys
    openai_api_key: Optional[str] = None
    paystack_secret_key: Optional[str] = None
    paypal_client_id: Optional[str] = None
    paypal_client_secret: Optional[str] = None
    
    # Database (if needed)
    database_url: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()