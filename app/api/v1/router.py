from fastapi import APIRouter
from app.api.v1.endpoints import generate, health, env_check

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(env_check.router, prefix="/env", tags=["environment"])
api_router.include_router(generate.router, prefix="/generate", tags=["generation"])