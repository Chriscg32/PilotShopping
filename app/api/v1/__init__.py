from fastapi import APIRouter
from .endpoints import generate, health, agents, tasks

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(generate.router, prefix="/generate", tags=["generate"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

__all__ = ["api_router"]