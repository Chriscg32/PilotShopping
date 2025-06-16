from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/env")
async def env_check():
    key_status = "Set" if settings.HUGGINGFACE_API_KEY else "Not Set"
    url_status = "Set" if settings.HUGGINGFACE_API_URL else "Not Set"
    return {
        "HUGGINGFACE_API_KEY": key_status,
        "HUGGINGFACE_API_URL": url_status
    }