from .base import database

def get_user_collection():
    return database.get_collection("users")  # Collection name for users

def get_item_collection():
    return database.get_collection("items")  # Collection name for items
