from pydantic import BaseModel, EmailStr, constr, validator

class RefreshTokenRequest(BaseModel):
    userID: str