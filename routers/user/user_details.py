from fastapi import APIRouter, HTTPException, Depends
from validations.user_details_validator import UserDetailsRequest
from decouple import config
from utils.mongo_utils import user_exists_by_id, get_user_by_id
from utils.token_utils import validate_token
from datetime import timedelta
from utils.enums import Roles
import typing as t
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
get_bearer_token = HTTPBearer(auto_error=False)

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("JWT_EXP_TIME"))

@router.post("/user-details", status_code=200)
async def user_details_route(user_details_request: UserDetailsRequest, auth: t.Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)):

    if not auth or not auth.credentials:
        raise HTTPException(status_code=401, detail="Invalid token")
    else:
        payload = validate_token(auth.credentials)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        elif(user_exists_by_id(payload["sub"]) and payload["sub"] == user_details_request.userID):
            #user_details = {"username": payload["sub"], "role": Roles.USER.value}
            user_details = get_user_by_id(payload["sub"])
            return user_details
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")