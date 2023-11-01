from pydantic import BaseModel, EmailStr, constr, validator

class UserLoginRequest(BaseModel):
    username: str
    password: str

    @validator("username")
    def username_valid(cls, username):
        # username validation logic here
        return username

    @validator("password")
    def password_valid(cls, password):
        # password validation logic here
        return password
