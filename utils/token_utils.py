import jwt
from datetime import datetime, timedelta
from decouple import config
from utils.enums import Roles

SECRET_KEY = config("JWT_SECRET")
ALGORITHM = config("JWT_ALGO")

def create_user_access_token(data: dict, expires_delta: timedelta = None):
    jwt_data = {"sub": data["userID"], "username": data["username"], "role": Roles.USER.value}
    to_encode = jwt_data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Invalid token
        return None
