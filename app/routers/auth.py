from fastapi import APIRouter, Depends
from app.core.security import get_current_user

router = APIRouter()

@router.post("/login")
async def login(credentials: LoginCredentials):
    # Login logic here
    pass

@router.get("/me")
async def get_current_user_info(current_user = Depends(get_current_user)):
    return current_user