from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_items():
    pass

@router.post("/")
async def create_item():
    pass

@router.get("/{item_id}")
async def get_item(item_id: int):
    pass