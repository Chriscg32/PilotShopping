from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.api.dependencies import get_environment_status
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.get("/")
async def check_environment(
    env_status: Dict[str, Any] = Depends(get_environment_status)
) -> Dict[str, Any]:
    """Check environment configuration and status."""
    logger.info("Environment check requested")
    
    return {
        "message": "Environment check completed",
        "environment": env_status
    }

@router.get("/validate")
async def validate_environment_endpoint() -> Dict[str, Any]:
    """Validate environment configuration."""
    from app.config import validate_environment
    
    validations = validate_environment()
    
    return {
        "message": "Environment validation completed",
        "validations": validations,
        "all_valid": all(validations.values())
    }