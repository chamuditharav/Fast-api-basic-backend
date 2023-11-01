from pymongo import MongoClient
import json
from decouple import config
import bcrypt

MONGO_URI = config("MONGO_URI")
MONGO_DB_NAME = config("MONGO_DB_NAME")
MONGO_USER_COLLECTION = config("MONGO_USER_COLLECTION")

client = MongoClient(MONGO_URI)
collection = client[MONGO_DB_NAME][MONGO_USER_COLLECTION]

def register_user(user_data):
    existing_user = collection.find_one({"username": user_data["username"]})
    if existing_user:
        return False  # User already exists

    inserted_user = collection.insert_one(user_data)
    return True  # User registration successful


def login_user(login_data):
    existing_user = collection.find_one({"username": login_data.username})
    if existing_user:
        # Use bcrypt's checkpw to verify the provided password against the hashed password
        hashed_password = existing_user.get("password", "")
        if bcrypt.checkpw(login_data.password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True  # User login successful

    return False  # Login failed

def hash_password(password):
    # Generate a salt and hash the password with bcrypt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password