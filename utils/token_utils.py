import jwt
from datetime import datetime, timedelta
from decouple import config

SECRET_KEY = config("JWT_SECRET")
ALGORITHM = config("JWT_ALGO")
ACCESS_TOKEN_EXPIRE_MINUTES = config("JWT_EXP_TIME")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
