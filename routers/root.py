from fastapi import APIRouter

router = APIRouter()

@router.get("/", status_code=200)
def read_root():
    return {"message": "Hello From The API 👋"}
