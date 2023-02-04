from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   tags=["products"],
                   responses={404: {"message": "No encontrado"}})

@router.get("/")
async def products():
    return ["product 1", "product 2", "product 3"]