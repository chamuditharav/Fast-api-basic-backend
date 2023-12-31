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
    existing_user = collection.find_one(
        {
            "$or": [
                {"username": user_data["username"]},
                {"email": user_data["email"]},
            ]
        }
    )

    if existing_user:
        if existing_user.get("username") == user_data["username"]:
            return "USERNAME_EXISTS"  # User with the same username already exists
        elif existing_user.get("email") == user_data["email"]:
            return "EMAIL_EXISTS"  # User with the same email already exists

    # Generate a unique userID
    user_data["userID"] = generate_unique_user_id()

    # Hash the user's password before storing it
    user_data["password"] = hash_password(user_data["password"])

    inserted_user = collection.insert_one(user_data)
    return "REGISTRATION_SUCCESS"  # User registration successful



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
    if user_data:
        user_data.pop("_id", None)
        user_data.pop("password", None)
    return user_data

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode()


if __name__ == "__main__":
    print(get_user_by_id("4dc7e721-0ec0-44e3-912c-5151d52c3613"))