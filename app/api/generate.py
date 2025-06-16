from fastapi import APIRouter

from config import settings

router = APIRouter()

@router.get("/generate")
async def generate_landing_copy():
    return {"copy": f"This is your generated landing page copy from {settings.app_name}."}