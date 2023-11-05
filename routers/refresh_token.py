from fastapi import APIRouter, HTTPException, Depends
from validations.refresh_token_validator import RefreshTokenRequest
from decouple import config
from utils.mongo_utils import get_user_by_id, user_exists_by_id
from utils.token_utils import validate_token, create_user_access_token
from datetime import timedelta
from utils.enums import Roles
from utils.rate_limiter import refresh_token_limter, init_rate_limiter
import typing as t
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
get_bearer_token = HTTPBearer(auto_error=False)

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("JWT_EXP_TIME"))

@router.on_event("startup")
async def startup():
    await init_rate_limiter()

@router.post("/refresh-token", status_code=200, dependencies=[Depends(refresh_token_limter)])
async def refresh_token_route(refresh_token_request: RefreshTokenRequest, auth: t.Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)):

    if not auth or not auth.credentials:
        raise HTTPException(status_code=401, detail="Invalid token")
    else:
        payload = validate_token(auth.credentials)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        elif(user_exists_by_id(payload["sub"]) and payload["sub"] == refresh_token_request.userID):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            user_data = get_user_by_id(payload["sub"])
            refreshed_token = create_user_access_token(
                                data= user_data,
                                expires_delta=access_token_expires,
                            )
            return {"refreshed_token": refreshed_token, "token_type": "bearer"}
        else:
             raise HTTPException(status_code=401, detail="Unauthorized")

            # user_details = {"username": payload["sub"], "role": Roles.USER.value}
            # return user_details
