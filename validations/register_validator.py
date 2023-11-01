
from utils.enums import Register
import re
from pydantic import BaseModel, EmailStr, constr, validator
from utils.enums import Register
import bleach
import bcrypt  # Import bcrypt for password hashing

class UserRegistrationRequest(BaseModel):
    username: constr(
        min_length=Register.USERNAME_MIN_LENGTH.value,
        max_length=Register.USERNAME_MAX_LENGTH.value,
    )
    password: constr(
        min_length=Register.PASSWORD_MIN_LENGTH.value,
        max_length=Register.PASSWORD_MAX_LENGTH.value,
    )
    email: EmailStr

    @validator("password")
    def validate_password(cls, value):
        # Define the regex pattern for alphanumeric and special characters
        pattern = r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[\W_]).*$'
        if not re.match(pattern, value):
            raise ValueError("Password must contain alphanumeric and special characters")
        # Hash the password before validation
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(value.encode('utf-8'), salt)
        return hashed_password.decode()

    @validator("username", "email")
    def sanitize_input(cls, value):
        # Use bleach to sanitize input and remove potential XSS payloads
        return bleach.clean(value)
