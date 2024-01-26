from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def read_home():
    return {"Home": "Page"}

@router.get("/items/{item_id}")
async def read_home_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}