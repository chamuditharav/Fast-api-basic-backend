from fastapi import APIRouter, HTTPException
from validations.login_validator import UserLoginRequest
from utils.mongo_utils import login_user
from utils.token_utils import create_access_token
from datetime import timedelta
from utils.enums import Roles

router = APIRouter()

@router.post("/user-login")
async def login_user_route(login_data: UserLoginRequest):
    if login_user(login_data):
        access_token_expires = timedelta(minutes=30)  # You can use a specific value here
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
