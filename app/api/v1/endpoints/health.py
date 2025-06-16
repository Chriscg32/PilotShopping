from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.api.dependencies import get_current_settings, validate_api_ready
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.get("/")
async def health_check(
    _: bool = Depends(validate_api_ready),
    settings: Dict[str, Any] = Depends(get_current_settings)
) -> Dict[str, Any]:
    """Basic health check endpoint."""
    logger.info("Health check requested")
    
    return {
        "status": "healthy",
        "app_name": settings["app_name"],
        "version": settings["version"],
        "environment": settings["environment"]
    }

@router.get("/detailed")
async def detailed_health_check(
    _: bool = Depends(validate_api_ready)
) -> Dict[str, Any]:
    """Detailed health check with system information."""
    from app.config import get_environment_info, validate_environment
    
    env_info = get_environment_info()
    validations = validate_environment()
    
    return {
        "status": "healthy",
        "environment": env_info,
        "validations": validations,
        "ready": all(validations.values())
    }