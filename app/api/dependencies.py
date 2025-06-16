from typing import Dict, Any
from fastapi import Depends, HTTPException, status
from app.config import settings, get_environment_info, validate_environment
from app.core.logger import get_logger

logger = get_logger(__name__)

async def get_current_settings() -> Dict[str, Any]:
    """Dependency to get current application settings."""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug
    }

async def validate_api_ready() -> bool:
    """Dependency to validate API readiness."""
    validations = validate_environment()
    
    if not validations["basic_config"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not properly configured"
        )
    
    return True

async def get_environment_status() -> Dict[str, Any]:
    """Dependency to get environment status."""
    return get_environment_info()