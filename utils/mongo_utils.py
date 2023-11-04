from pymongo import MongoClient
import json
from decouple import config
import bcrypt
import uuid

MONGO_URI = config("MONGO_URI")
MONGO_DB_NAME = config("MONGO_DB_NAME")
MONGO_USER_COLLECTION = config("MONGO_USER_COLLECTION")

client = MongoClient(MONGO_URI)
collection = client[MONGO_DB_NAME][MONGO_USER_COLLECTION]

def generate_unique_user_id():
    while True:
        user_id = str(uuid.uuid4())
        if collection.find_one({"userID": user_id}) is None:
            return user_id

def register_user(user_data):
    existing_user = collection.find_one({"username": user_data["username"]})
    if existing_user:
        return False  # User already exists

    # Generate a unique userID
    user_data["userID"] = generate_unique_user_id()

    # Hash the user's password before storing it
    user_data["password"] = hash_password(user_data["password"])

    inserted_user = collection.insert_one(user_data)
    return True  # User registration successful


def login_user(login_data):
    existing_user = collection.find_one(
        {
            "$or": [
                {"username": login_data.username},
                {"email": login_data.username},
            ]
        }
    )
    if existing_user:
        hashed_password = existing_user.get("password", "")
        if bcrypt.checkpw(login_data.password.encode('utf-8'), hashed_password.encode('utf-8')):
            return existing_user
    return None

def user_exists_by_id(user_id):
    existing_user = collection.find_one({"userID": user_id})
    return existing_user is not None

def get_user_by_id(user_id):
    user_data = collection.find_one({"userID": user_id})
    return user_data

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode()
