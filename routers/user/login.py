from fastapi import APIRouter, HTTPException, Depends
from validations.login_validator import UserLoginRequest
from decouple import config
from utils.mongo_utils import login_user
from utils.token_utils import create_access_token
from datetime import timedelta
from utils.enums import Roles

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("JWT_EXP_TIME"))


@router.post("/user-login")
async def login_user_route(login_data: UserLoginRequest):
    if login_user(login_data):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # You can use a specific value here
        access_token = create_access_token(
            data={
                "sub": login_data.username,
                "role": Roles.USER.value
                },
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Login failed")
