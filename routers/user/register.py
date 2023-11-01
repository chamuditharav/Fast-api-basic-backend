# routers/register.py

from fastapi import APIRouter, HTTPException, Depends
from utils.mongo_utils import register_user
from utils.enums import Register
from validations.register_validator import UserRegistrationRequest
from utils.rate_limiter import register_limiter, init_rate_limiter

router = APIRouter()

@router.post("/user-register", status_code=201, dependencies=[Depends(register_limiter)])
async def register_user_endpoint(user_data: UserRegistrationRequest):
    user_data_dict = user_data.dict()
    if not register_user(user_data_dict):
        raise HTTPException(status_code=400, detail="Username already exists")

    return {"message": "User registration successful"}
