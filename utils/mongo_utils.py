from pymongo import MongoClient
import json
from decouple import config


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
    existing_user = collection.find_one({"username": login_data.username, "password": login_data.password})
    if existing_user:
        return True  # User login successful
    return False  # Login failed