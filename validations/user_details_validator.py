from pydantic import BaseModel, EmailStr, constr, validator

class UserDetailsRequest(BaseModel):
    userID: str